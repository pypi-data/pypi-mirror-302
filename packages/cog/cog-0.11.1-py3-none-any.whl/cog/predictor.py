import builtins
import enum
import importlib.util
import inspect
import io
import os.path
import sys
import types
import uuid
from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator
from pathlib import Path
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    Union,
    cast,
)

try:
    from typing import Literal, get_args, get_origin
except ImportError:  # Python < 3.8
    from typing_compat import get_args, get_origin  # type: ignore
    from typing_extensions import Literal

from unittest.mock import patch

import pydantic
import structlog
import yaml
from pydantic import BaseModel, Field, create_model
from pydantic.fields import FieldInfo

# Added in Python 3.9. Can be from typing if we drop support for <3.9
from typing_extensions import Annotated

from .code_xforms import load_module_from_string, strip_model_source_code
from .errors import ConfigDoesNotExist, PredictorNotSet
from .types import (
    PYDANTIC_V2,
    CogConfig,
    Input,
    URLPath,
)
from .types import (
    File as CogFile,
)
from .types import (
    Path as CogPath,
)
from .types import Secret as CogSecret

log = structlog.get_logger("cog.server.predictor")

ALLOWED_INPUT_TYPES: List[Type[Any]] = [
    str,
    int,
    float,
    bool,
    CogFile,
    CogPath,
    CogSecret,
]


class BasePredictor(ABC):
    def setup(
        self,
        weights: Optional[Union[CogFile, CogPath, str]] = None,  # pylint: disable=unused-argument
    ) -> None:
        """
        An optional method to prepare the model so multiple predictions run efficiently.
        """
        return

    @abstractmethod
    def predict(self, **kwargs: Any) -> Any:
        """
        Run a single prediction on the model
        """


def run_setup(predictor: BasePredictor) -> None:
    weights_type = get_weights_type(predictor.setup)

    # No weights need to be passed, so just run setup() without any arguments.
    if weights_type is None:
        predictor.setup()
        return

    weights: Union[io.IOBase, Path, str, None]

    weights_url = os.environ.get("COG_WEIGHTS")
    weights_path = "weights"

    # TODO: Cog{File,Path}.validate(...) methods accept either "real"
    # paths/files or URLs to those things. In future we can probably tidy this
    # up a little bit.
    # TODO: CogFile/CogPath should have subclasses for each of the subtypes
    if weights_url:
        if PYDANTIC_V2:
            from pydantic import TypeAdapter

            for t in [CogFile, CogPath]:
                try:
                    weights = TypeAdapter(t).validate_python(weights_url)
                    break
                except Exception:  # pylint: disable=broad-except # noqa: S110
                    pass
            else:
                if weights_type is str:
                    weights = weights_url
                else:
                    raise ValueError(
                        f"Predictor.setup() has an argument 'weights' of type {weights_type}, but only File, Path and str are supported"
                    )
        else:
            if weights_type is CogFile:
                weights = cast(CogFile, CogFile.validate(weights_url))
            elif weights_type is CogPath:
                # TODO: So this can be a url. evil!
                weights = cast(CogPath, CogPath.validate(weights_url))
            elif weights_type is str:
                weights = weights_url
            else:
                raise ValueError(
                    f"Predictor.setup() has an argument 'weights' of type {weights_type}, but only File, Path and str are supported"
                )
    elif os.path.exists(weights_path):
        if weights_type == CogFile:
            with open(weights_path, "rb") as f:
                weights = cast(CogFile, f)
        elif weights_type == CogPath:
            weights = CogPath(weights_path)
        else:
            raise ValueError(
                f"Predictor.setup() has an argument 'weights' of type {weights_type}, but only File, Path and str are supported"
            )
    else:
        weights = None

    predictor.setup(weights=weights)  # type: ignore


def get_weights_type(setup_function: Callable[[Any], None]) -> Optional[Any]:
    signature = inspect.signature(setup_function)
    if "weights" not in signature.parameters:
        return None
    Type = signature.parameters["weights"].annotation  # pylint: disable=invalid-name,redefined-outer-name
    # Handle Optional. It is Union[Type, None]
    if get_origin(Type) == Union:
        args = get_args(Type)
        if len(args) == 2 and args[1] is type(None):
            Type = get_args(Type)[0]  # pylint: disable=invalid-name
    return Type


def load_config() -> CogConfig:
    """
    Reads cog.yaml and returns it as a typed dict.
    """
    # Assumes the working directory is /src
    config_path = os.path.abspath("cog.yaml")
    try:
        with open(config_path, encoding="utf-8") as fh:
            config = yaml.safe_load(fh)
    except FileNotFoundError as e:
        raise ConfigDoesNotExist(
            f"Could not find {config_path}",
        ) from e
    return config


def load_predictor(config: CogConfig) -> BasePredictor:
    """
    Constructs an instance of the user-defined Predictor class from a config.
    """

    ref = get_predictor_ref(config)
    return load_predictor_from_ref(ref)


def get_predictor_ref(config: CogConfig, mode: str = "predict") -> str:
    if mode not in ["predict", "train"]:
        raise ValueError(f"Invalid mode: {mode}")

    if mode not in config:
        raise PredictorNotSet(
            f"Can't run predictions: '{mode}' option not found in cog.yaml"
        )

    return config[mode]


def load_full_predictor_from_file(
    module_path: str, module_name: str
) -> types.ModuleType:
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    # Remove any sys.argv while importing predictor to avoid conflicts when
    # user code calls argparse.Parser.parse_args in production
    with patch("sys.argv", sys.argv[:1]):
        spec.loader.exec_module(module)
    return module


def load_slim_predictor_from_file(
    module_path: str, class_name: str, method_name: str
) -> Optional[types.ModuleType]:
    with open(module_path, encoding="utf-8") as file:
        source_code = file.read()
    stripped_source = strip_model_source_code(source_code, class_name, method_name)
    module = load_module_from_string(uuid.uuid4().hex, stripped_source)
    return module


def get_predictor(module: types.ModuleType, class_name: str) -> Any:
    predictor = getattr(module, class_name)
    # It could be a class or a function
    if inspect.isclass(predictor):
        return predictor()
    return predictor


def load_slim_predictor_from_ref(ref: str, method_name: str) -> BasePredictor:
    module_path, class_name = ref.split(":", 1)
    module_name = os.path.basename(module_path).split(".py", 1)[0]
    module = None
    try:
        if sys.version_info >= (3, 9):
            module = load_slim_predictor_from_file(module_path, class_name, method_name)
            if not module:
                log.debug(f"[{module_name}] fast loader returned None")
        else:
            log.debug(f"[{module_name}] cannot use fast loader as current Python <3.9")
    except Exception as e:  # pylint: disable=broad-exception-caught
        log.debug(f"[{module_name}] fast loader failed: {e}")
    finally:
        if not module:
            log.debug(f"[{module_name}] falling back to slow loader")
            module = load_full_predictor_from_file(module_path, module_name)
    predictor = get_predictor(module, class_name)
    return predictor


def load_predictor_from_ref(ref: str) -> BasePredictor:
    module_path, class_name = ref.split(":", 1)
    module_name = os.path.basename(module_path).split(".py", 1)[0]
    module = load_full_predictor_from_file(module_path, module_name)
    predictor = get_predictor(module, class_name)
    return predictor


# Base class for inputs, constructed dynamically in get_input_type().
# (This can't be a docstring or it gets passed through to the schema.)
class BaseInput(BaseModel):
    if PYDANTIC_V2:
        model_config = pydantic.ConfigDict(use_enum_values=True)  # type: ignore
    else:

        class Config:
            # When using `choices`, the type is converted into an enum to validate
            # But, after validation, we want to pass the actual value to predict(), not the enum object
            use_enum_values = True

    def cleanup(self) -> None:
        """
        Cleanup any temporary files created by the input.
        """

        for _, value in dict(self).items():
            # Handle URLPath objects specially for cleanup.
            # Also handle pathlib.Path objects, which cog.Path is a subclass of.
            # A pathlib.Path object shouldn't make its way here,
            # but both have an unlink() method, so we may as well be safe.
            if isinstance(value, (URLPath, Path)):
                # TODO: use unlink(missing_ok=...) when we drop Python 3.7 support.
                try:
                    value.unlink()
                except FileNotFoundError:
                    pass


def validate_input_type(
    type: Type[Any],  # pylint: disable=redefined-builtin
    name: str,
) -> None:
    if type is inspect.Signature.empty:
        raise TypeError(
            f"No input type provided for parameter `{name}`. Supported input types are: {readable_types_list(ALLOWED_INPUT_TYPES)}, or a Union or List of those types."
        )
    if type not in ALLOWED_INPUT_TYPES:
        if get_origin(type) is Literal:
            for t in get_args(type):
                validate_input_type(builtins.type(t), name)
        elif get_origin(type) in (Union, List, list) or (
            hasattr(types, "UnionType") and get_origin(type) is types.UnionType
        ):  # noqa: E721
            for t in get_args(type):
                validate_input_type(t, name)
        else:
            if PYDANTIC_V2:
                # Cog types are exported as `Annotated[Type, ...]`, but `type` is the inner type
                if hasattr(type, "__module__") and type.__module__ == "cog.types":
                    return

            raise TypeError(
                f"Unsupported input type {human_readable_type_name(type)} for parameter `{name}`. Supported input types are: {readable_types_list(ALLOWED_INPUT_TYPES)}, or a Union or List of those types."
            )


def get_input_create_model_kwargs(signature: inspect.Signature) -> Dict[str, Any]:
    create_model_kwargs = {}

    order = 0

    for name, parameter in signature.parameters.items():
        InputType = parameter.annotation

        validate_input_type(InputType, name)

        # if no default is specified, create an empty, required input
        if parameter.default is inspect.Signature.empty:
            default = Input()
        else:
            if not isinstance(parameter.default, FieldInfo):
                default = Input(default=parameter.default)
            else:
                default = parameter.default

        if PYDANTIC_V2:
            # https://github.com/pydantic/pydantic/blob/2.7/pydantic/json_schema.py#L1436-L1446
            # json_schema_extra can be a callable, but we don't set that and users shouldn't set that
            if not default.json_schema_extra:  # type: ignore
                default.json_schema_extra = {}  # type: ignore
            assert isinstance(default.json_schema_extra, dict)  # type: ignore
            extra = default.json_schema_extra  # type: ignore
        else:
            extra = default.extra  # type: ignore
        extra["x-order"] = order
        order += 1

        # Choices!
        choices = (
            extra.pop("choices", None)  # Pydantic v1
            or extra.pop("enum", None)  # Pydantic v2
        )
        # In either case, remove it as an extra field because it will be
        # passed automatically as 'enum' in the schema
        if choices:
            if InputType == str and isinstance(choices, Iterable):  # noqa: E721

                class StringEnum(str, enum.Enum):
                    pass

                InputType = StringEnum(  # pylint: disable=invalid-name
                    name, [(value, value) for value in choices or []]
                )
            elif InputType == int:  # noqa: E721
                InputType = enum.IntEnum(name, {str(value): value for value in choices})  # type: ignore # pylint: disable=invalid-name
            else:
                raise TypeError(
                    f"The input {name} uses the option choices. Choices can only be used with str or int types."
                )

        create_model_kwargs[name] = (InputType, default)

    return create_model_kwargs


def get_predict(predictor: Any) -> Callable[..., Any]:
    if hasattr(predictor, "predict"):
        return predictor.predict
    return predictor


def get_input_type(predictor: BasePredictor) -> Type[BaseInput]:
    """
    Creates a Pydantic Input model from the arguments of a Predictor's predict() method.

    class Predictor(BasePredictor):
        def predict(self, text: str):
            ...

    programmatically creates a model like this:

    class Input(BaseModel):
        text: str
    """

    predict = get_predict(predictor)
    signature = inspect.signature(predict)

    return create_model(
        "Input",
        __config__=None,
        __base__=BaseInput,
        __module__=__name__,
        __validators__=None,
        **get_input_create_model_kwargs(signature),
    )  # type: ignore


def get_output_type(predictor: BasePredictor) -> Type[BaseModel]:
    """
    Creates a Pydantic Output model from the return type annotation of a Predictor's predict() method.
    """

    predict = get_predict(predictor)
    signature = inspect.signature(predict)
    OutputType: Type[BaseModel]
    if signature.return_annotation is inspect.Signature.empty:
        raise TypeError(
            """You must set an output type. If your model can return multiple output types, you can explicitly set `Any` as the output type.

For example:

    from typing import Any

    def predict(
        self,
        image: Path = Input(description="Input image"),
    ) -> Any:
        ...
"""
        )
    else:
        OutputType = signature.return_annotation

    # The type that goes in the response is a list of the yielded type
    if get_origin(OutputType) is Iterator:
        # Annotated allows us to attach Field annotations to the list, which we use to mark that this is an iterator
        # https://pydantic-docs.helpmanual.io/usage/schema/#typingannotated-fields
        if PYDANTIC_V2:
            field = Field(**{"json_schema_extra": {"x-cog-array-type": "iterator"}})  # type: ignore
        else:
            field = Field(**{"x-cog-array-type": "iterator"})  # type: ignore
        OutputType: Type[BaseModel] = Annotated[List[get_args(OutputType)[0]], field]  # type: ignore

    name = OutputType.__name__ if hasattr(OutputType, "__name__") else ""

    if name == "Output":
        return OutputType

    # We wrap the OutputType in an Output class to
    # ensure consistent naming of the interface in the schema.
    #
    # NOTE: If the OutputType.__name__ is "TrainingOutput" then cannot use
    # `__root__` here because this will create a reference for the Object.
    # e.g.
    #   {'title': 'Output', '$ref': '#/definitions/TrainingOutput' ... }
    #
    # And this reference may conflict with other objects at which
    # point the item will be namespaced and break our parsing. e.g.
    #   {'title': 'Output', '$ref': '#/definitions/predict_TrainingOutput' ... }
    #
    # So we work around this by inheriting from the original class rather
    # than using "__root__".
    if name == "TrainingOutput":  # pylint: disable=no-else-return

        class Output(OutputType):  # type: ignore
            pass

        return Output
    else:
        if PYDANTIC_V2:

            class Output(pydantic.RootModel[OutputType]):  # type: ignore
                pass
        else:

            class Output(BaseModel):
                __root__: OutputType  # type: ignore

        return Output


def get_train(predictor: Any) -> Callable[..., Any]:
    if hasattr(predictor, "train"):
        return predictor.train
    return predictor


def get_training_input_type(predictor: BasePredictor) -> Type[BaseInput]:
    """
    Creates a Pydantic Input model from the arguments of a Predictor's train() method.

    def train(self, text: str):
        ...

    programmatically creates a model like this:

    class TrainingInput(BaseModel):
        text: str
    """

    train = get_train(predictor)
    signature = inspect.signature(train)

    return create_model(
        "TrainingInput",
        __config__=None,
        __base__=BaseInput,
        __module__=__name__,
        __validators__=None,
        **get_input_create_model_kwargs(signature),
    )  # type: ignore


def get_training_output_type(predictor: BasePredictor) -> Type[BaseModel]:
    """
    Creates a Pydantic Output model from the return type annotation of a train() method.
    """

    train = get_train(predictor)
    signature = inspect.signature(train)

    if signature.return_annotation is inspect.Signature.empty:
        raise TypeError(
            """You must set an output type. If your model can return multiple output types, you can explicitly set `Any` as the output type.

For example:

    from typing import Any

    def train(
        self,
        n: int
    ) -> Any:
        ...
"""
        )
    else:
        TrainingOutputType = signature.return_annotation

    name = (
        TrainingOutputType.__name__ if hasattr(TrainingOutputType, "__name__") else ""
    )

    # We wrap the OutputType in a TrainingOutput class to
    # ensure consistent naming of the interface in the schema
    # See comment in get_output_type for more info.
    if name == "TrainingOutput":
        return TrainingOutputType

    if name == "Output":  # pylint: disable=no-else-return

        class TrainingOutput(TrainingOutputType):  # type: ignore
            pass

        return TrainingOutput
    else:
        if PYDANTIC_V2:

            class TrainingOutput(pydantic.RootModel[TrainingOutputType]):  # type: ignore
                pass

            return TrainingOutput

        else:

            class TrainingOutput(BaseModel):
                __root__: TrainingOutputType  # type: ignore

            return TrainingOutput


def human_readable_type_name(t: Type[Union[Any, None]]) -> str:
    """
    Generates a useful-for-humans label for a type. For builtin types, it's just the class name (eg "str" or "int"). For other types, it includes the module (eg "pathlib.Path" or "cog.File").

    The special case for Cog modules is because the type lives in `cog.types` internally, but just `cog` when included as a dependency.
    """

    if hasattr(t, "__module__"):
        module = t.__module__

        if module == "builtins":
            return t.__qualname__

        if module.split(".")[0] == "cog":
            module = "cog"

        try:
            return f"{module}.{t.__qualname__}"
        except AttributeError:
            pass

    return str(t)


def readable_types_list(type_list: List[Type[Any]]) -> str:
    return ", ".join(human_readable_type_name(t) for t in type_list)
