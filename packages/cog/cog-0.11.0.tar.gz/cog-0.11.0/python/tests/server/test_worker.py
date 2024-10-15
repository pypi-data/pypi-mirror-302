import multiprocessing
import os
import threading
import time
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import pytest
from attrs import define, evolve, field, frozen
from hypothesis import HealthCheck, given, settings
from hypothesis import strategies as st
from hypothesis.stateful import (
    Bundle,
    RuleBasedStateMachine,
    consumes,
    multiple,
    rule,
)

from cog.server.eventtypes import Done, Log, PredictionOutput, PredictionOutputType
from cog.server.exceptions import FatalWorkerException, InvalidStateException
from cog.server.worker import Worker, _PublicEventType

from .conftest import WorkerConfig, uses_worker

if TYPE_CHECKING:
    from concurrent.futures import Future

# Set a longer deadline on CI as the instances are a bit slower.
settings.register_profile("ci", max_examples=200, deadline=2000)
settings.register_profile("default", max_examples=50, deadline=1500)
settings.load_profile(os.getenv("HYPOTHESIS_PROFILE", "default"))

HYPOTHESIS_TEST_TIMEOUT = (
    settings().max_examples * settings().deadline
).total_seconds() + 5

ST_NAMES = st.sampled_from(["John", "Barry", "Elspeth", "Hamid", "Ronnie", "Yasmeen"])

SETUP_FATAL_FIXTURES = [
    "exc_in_setup",
    "exc_in_setup_and_predict",
    "exc_on_import",
    "exit_in_setup",
    "exit_on_import",
    "missing_predictor",
    "nonexistent_file",
]

PREDICTION_FATAL_FIXTURES = [
    "exit_in_predict",
    "killed_in_predict",
]

RUNNABLE_FIXTURES = [
    "simple",
    "exc_in_predict",
    "missing_predict",
]

OUTPUT_FIXTURES = [
    (
        WorkerConfig("hello_world"),
        {"name": ST_NAMES},
        lambda x: f"hello, {x['name']}",
    ),
    (
        WorkerConfig("count_up"),
        {"upto": st.integers(min_value=0, max_value=100)},
        lambda x: list(range(x["upto"])),
    ),
    (
        WorkerConfig("complex_output"),
        {},
        lambda _: {"number": 42, "text": "meaning of life"},
    ),
]

SETUP_LOGS_FIXTURES = [
    (
        (
            "writing some stuff from C at import time\n"
            "writing to stdout at import time\n"
            "setting up predictor\n"
        ),
        "writing to stderr at import time\n",
    )
]

PREDICT_LOGS_FIXTURES = [
    (
        ("writing from C\n" "writing with print\n"),
        ("WARNING:root:writing log message\n" "writing to stderr\n"),
    )
]


@define
class Result:
    stdout_lines: List[str] = field(factory=list)
    stderr_lines: List[str] = field(factory=list)
    heartbeat_count: int = 0
    output_type: Optional[PredictionOutputType] = None
    output: Any = None
    done: Optional[Done] = None
    exception: Optional[Exception] = None

    @property
    def stdout(self):
        return "".join(self.stdout_lines)

    @property
    def stderr(self):
        return "".join(self.stderr_lines)

    def handle_event(self, event: _PublicEventType):
        if isinstance(event, Log) and event.source == "stdout":
            self.stdout_lines.append(event.message)
        elif isinstance(event, Log) and event.source == "stderr":
            self.stderr_lines.append(event.message)
        elif isinstance(event, Done):
            assert not self.done
            self.done = event
        elif isinstance(event, PredictionOutput):
            assert self.output_type, "Should get output type before any output"
            if self.output_type.multi:
                self.output.append(event.payload)
            else:
                assert (
                    self.output is None
                ), "Should not get multiple outputs for output type single"
                self.output = event.payload
        elif isinstance(event, PredictionOutputType):
            assert (
                self.output_type is None
            ), "Should not get multiple output type events"
            self.output_type = event
            if self.output_type.multi:
                self.output = []
        else:
            pytest.fail(f"saw unexpected event: {event}")


def _process(worker, work, swallow_exceptions=False):
    """
    Helper function to collect events generated by Worker during tests.
    """
    result = Result()
    subid = worker.subscribe(result.handle_event)
    try:
        work().result()
    except Exception as exc:
        result.exception = exc
        if not swallow_exceptions:
            raise
    finally:
        worker.unsubscribe(subid)
    return result


@uses_worker(SETUP_FATAL_FIXTURES, setup=False)
def test_fatalworkerexception_from_setup_failures(worker):
    """
    Any failure during setup is fatal and should raise FatalWorkerException.
    """
    with pytest.raises(FatalWorkerException):
        _process(worker, worker.setup)


@uses_worker(PREDICTION_FATAL_FIXTURES)
def test_fatalworkerexception_from_irrecoverable_failures(worker):
    """
    Certain kinds of failure during predict (crashes, unexpected exits) are
    irrecoverable and should raise FatalWorkerException.
    """
    with pytest.raises(FatalWorkerException):
        _process(worker, lambda: worker.predict({}))

    with pytest.raises(InvalidStateException):
        _process(worker, lambda: worker.predict({}))


@uses_worker(RUNNABLE_FIXTURES)
def test_no_exceptions_from_recoverable_failures(worker):
    """
    Well-behaved predictors, or those that only throw exceptions, should not
    raise.
    """
    for _ in range(5):
        _process(worker, lambda: worker.predict({}))


@uses_worker("stream_redirector_race_condition")
def test_stream_redirector_race_condition(worker):
    """
    StreamRedirector and ChildWorker are using the same pipe to send data. When
    there are multiple threads trying to write to the same pipe, it can cause
    data corruption by race condition. The data corruption will cause pipe
    receiver to raise an exception due to unpickling error.
    """
    for _ in range(5):
        result = _process(worker, lambda: worker.predict({}))
        assert not result.done.error


@pytest.mark.timeout(HYPOTHESIS_TEST_TIMEOUT)
@pytest.mark.parametrize(
    "worker,payloads,output_generator", OUTPUT_FIXTURES, indirect=["worker"]
)
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
@given(data=st.data())
def test_output(worker, payloads, output_generator, data):
    """
    We should get the outputs we expect from predictors that generate output.

    Note that most of the validation work here is actually done in _process.
    """
    payload = data.draw(st.fixed_dictionaries(payloads))
    expected_output = output_generator(payload)

    result = _process(worker, lambda: worker.predict(payload))

    assert result.output == expected_output


@uses_worker("logging", setup=False)
@pytest.mark.parametrize("expected_stdout,expected_stderr", SETUP_LOGS_FIXTURES)
def test_setup_logging(worker, expected_stdout, expected_stderr):
    """
    We should get the logs we expect from predictors that generate logs during
    setup.
    """
    result = _process(worker, worker.setup)
    assert not result.done.error

    assert result.stdout == expected_stdout
    assert result.stderr == expected_stderr


@uses_worker("logging")
@pytest.mark.parametrize("expected_stdout,expected_stderr", PREDICT_LOGS_FIXTURES)
def test_predict_logging(worker, expected_stdout, expected_stderr):
    """
    We should get the logs we expect from predictors that generate logs during
    predict.
    """
    result = _process(worker, lambda: worker.predict({}))

    assert result.stdout == expected_stdout
    assert result.stderr == expected_stderr


@uses_worker("sleep", setup=False)
def test_cancel_is_safe(worker):
    """
    Calls to cancel at any time should not result in unexpected things
    happening or the cancelation of unexpected predictions.
    """

    for _ in range(50):
        worker.cancel()

    result = _process(worker, worker.setup)
    assert not result.done.error

    for _ in range(50):
        worker.cancel()

    result1 = _process(
        worker, lambda: worker.predict({"sleep": 0.5}), swallow_exceptions=True
    )

    for _ in range(50):
        worker.cancel()

    result2 = _process(
        worker, lambda: worker.predict({"sleep": 0.1}), swallow_exceptions=True
    )

    assert not result1.exception
    assert not result1.done.canceled
    assert not result2.exception
    assert not result2.done.canceled
    assert result2.output == "done in 0.1 seconds"


@uses_worker("sleep", setup=False)
def test_cancel_idempotency(worker):
    """
    Multiple calls to cancel within the same prediction, while not necessary or
    recommended, should still only result in a single cancelled prediction, and
    should not affect subsequent predictions.
    """

    def cancel_a_bunch(_):
        for _ in range(100):
            worker.cancel()

    result = _process(worker, worker.setup)
    assert not result.done.error

    fut = worker.predict({"sleep": 0.5})
    # We call cancel a WHOLE BUNCH to make sure that we don't propagate any
    # of those cancelations to subsequent predictions, regardless of the
    # internal implementation of exceptions raised inside signal handlers.
    for _ in range(5):
        time.sleep(0.05)
        for _ in range(100):
            worker.cancel()
    result1 = fut.result()
    assert result1.canceled

    result2 = _process(worker, lambda: worker.predict({"sleep": 0.1}))

    assert not result2.done.canceled
    assert result2.output == "done in 0.1 seconds"


@uses_worker("sleep")
def test_cancel_multiple_predictions(worker):
    """
    Multiple predictions cancelled in a row shouldn't be a problem. This test
    is mainly ensuring that the _allow_cancel latch in Worker is correctly
    reset every time a prediction starts.
    """
    dones: list[Done] = []
    for _ in range(5):
        fut = worker.predict({"sleep": 1})
        time.sleep(0.1)
        worker.cancel()
        dones.append(fut.result())
    assert dones == [Done(canceled=True)] * 5

    assert not worker.predict({"sleep": 0}).result().canceled


@uses_worker("sleep")
def test_graceful_shutdown(worker):
    """
    On shutdown, the worker should finish running the current prediction, and
    then exit.
    """

    saw_first_event = threading.Event()

    # When we see the first event, we'll start the shutdown process.
    worker.subscribe(lambda event: saw_first_event.set())

    fut = worker.predict({"sleep": 1})

    saw_first_event.wait(timeout=1)
    worker.shutdown(timeout=2)

    assert fut.result() == Done()


@frozen
class SetupState:
    fut: "Future[Done]"
    result: Result

    error: bool = False


@frozen
class PredictState:
    payload: Dict[str, Any]
    fut: "Future[Done]"
    result: Result

    canceled: bool = False
    error: bool = False


class FakeChildWorker:
    exitcode = None
    cancel_sent = False
    alive = True

    def start(self):
        pass

    def is_alive(self):
        return self.alive

    def send_cancel(self):
        self.cancel_sent = True

    def terminate(self):
        pass

    def join(self):
        pass


class WorkerStateMachine(RuleBasedStateMachine):
    """
    This is a Hypothesis-driven rule-based state machine test. It is intended
    to ensure that any sequence of calls to the public API of Worker leaves the
    instance in an expected state.

    In short: any call should either throw InvalidStateException or should do
    what the caller asked.

    See https://hypothesis.readthedocs.io/en/latest/stateful.html for more on
    stateful testing with Hypothesis.
    """

    predict_pending = Bundle("predict_pending")
    predict_complete = Bundle("predict_complete")
    setup_pending = Bundle("setup_pending")
    setup_complete = Bundle("setup_complete")

    def __init__(self):
        super().__init__()

        parent_conn, child_conn = multiprocessing.get_context("spawn").Pipe()
        parent_conn.send = lambda x: None  # FIXME: do something less awful

        self.child = FakeChildWorker()
        self.child_events = child_conn

        self.pending = threading.Semaphore(0)

        self.worker = Worker(child=self.child, events=parent_conn)

    def simulate_events(self, events, *, target=None):
        def _handle_event(ev):
            if target:
                target.handle_event(ev)
            self.pending.release()

        subid = self.worker.subscribe(_handle_event)
        try:
            for event in events:
                self.child_events.send(event)
                self.pending.acquire()
        finally:
            self.worker.unsubscribe(subid)

    @rule(target=setup_pending)
    def setup(self):
        try:
            fut = self.worker.setup()
        except InvalidStateException:
            return multiple()
        else:
            return SetupState(fut=fut, result=Result())

    @rule(
        state=setup_pending,
        text=st.text(),
        source=st.sampled_from(["stdout", "stderr"]),
    )
    def simulate_setup_logs(self, state: SetupState, text: str, source: str):
        events = [Log(source=source, message=text)]
        self.simulate_events(events, target=state.result)

    @rule(state=consumes(setup_pending), target=setup_complete)
    def simulate_setup_success(self, state: SetupState):
        self.simulate_events(events=[Done()], target=state.result)
        return state

    @rule(state=consumes(setup_pending), target=setup_complete)
    def simulate_setup_failure(self, state: SetupState):
        self.simulate_events(
            events=[Done(error=True, error_detail="Setup failed!")],
            target=state.result,
        )
        return evolve(state, error=True)

    @rule(state=consumes(setup_complete))
    def await_setup(self, state: SetupState):
        if state.error:
            with pytest.raises(FatalWorkerException):
                state.fut.result()
            assert state.result.done.error
            assert state.result.done.error_detail == "Setup failed!"
        else:
            ev = state.fut.result()
            assert isinstance(ev, Done)
            assert state.result.done == Done()

    @rule(
        target=predict_pending,
        name=ST_NAMES,
        steps=st.integers(min_value=0, max_value=5),
    )
    def predict(self, name: str, steps: int) -> PredictState:
        payload = {"name": name, "steps": steps}
        try:
            fut = self.worker.predict(payload)
        except InvalidStateException:
            return multiple()
        else:
            return PredictState(payload=payload, fut=fut, result=Result())

    @rule(
        state=predict_pending,
        text=st.text(),
        source=st.sampled_from(["stdout", "stderr"]),
    )
    def simulate_predict_logs(self, state: PredictState, text: str, source: str):
        events = [Log(source=source, message=text)]
        self.simulate_events(events, target=state.result)

    @rule(state=consumes(predict_pending), target=predict_complete)
    def simulate_predict_success(self, state: PredictState):
        events = []

        steps = state.payload["steps"]
        name = state.payload["name"]

        if steps == 1:
            events.append(PredictionOutputType(multi=False))
            events.append(PredictionOutput(payload=f"NAME={name}"))

        elif steps > 1:
            events.append(PredictionOutputType(multi=True))
            for i in range(steps):
                events.append(PredictionOutput(payload=f"NAME={name},STEP={i+1}"))

        events.append(Done(canceled=state.canceled))

        self.simulate_events(events, target=state.result)
        return state

    @rule(state=consumes(predict_pending), target=predict_complete)
    def simulate_predict_failure(self, state: PredictState):
        events = [
            Done(
                error=True,
                error_detail="Kaboom!",
                canceled=state.canceled,
            )
        ]

        self.simulate_events(events, target=state.result)
        return evolve(state, error=True)

    @rule(state=consumes(predict_complete))
    def await_predict(self, state: PredictState):
        ev = state.fut.result()
        assert isinstance(ev, Done)
        assert state.result.done

        if state.canceled:
            assert state.result.done.canceled
            return

        if state.error:
            assert state.result.done.error
            assert state.result.done.error_detail == "Kaboom!"
            return

        steps = state.payload["steps"]
        name = state.payload["name"]

        if steps == 0:
            assert not state.result.output
        elif steps == 1:
            assert state.result.output == f"NAME={name}"
        else:
            assert state.result.output == [
                f"NAME={name},STEP={i+1}" for i in range(steps)
            ]

        assert state.result.done == Done()

    # For now, we only try canceling when we know a prediction is running.
    @rule(
        target=predict_pending,
        state=consumes(predict_pending),
    )
    def cancel(self, state: PredictState):
        self.worker.cancel()
        return evolve(state, canceled=True)

    def teardown(self):
        self.child.alive = False
        self.worker.shutdown()


# Set a longer timeout for the state machine test. It can take a little while,
# particularly in CI, and particularly if it finds a failure, as shrinking
# might not happen all that quickly.
TestWorkerState = pytest.mark.timeout(600)(WorkerStateMachine.TestCase)
