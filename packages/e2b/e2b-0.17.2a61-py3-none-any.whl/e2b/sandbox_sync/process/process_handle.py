from typing import Optional, Callable, Any, Generator, Union, Tuple

from e2b.envd.rpc import handle_rpc_exception
from e2b.envd.process import process_pb2
from e2b.sandbox.process.process_handle import (
    ProcessExitException,
    ProcessResult,
    Stderr,
    Stdout,
    PtyOutput,
)


class ProcessHandle:
    """
    Class representing a process. It provides methods for waiting and killing the process.
    It is also used to iterate over the process output.
    """

    @property
    def pid(self):
        """
        Get the process ID.
        """
        return self._pid

    def __init__(
        self,
        pid: int,
        handle_kill: Callable[[], bool],
        events: Generator[
            Union[process_pb2.StartResponse, process_pb2.ConnectResponse], Any, None
        ],
    ):
        self._pid = pid
        self._handle_kill = handle_kill
        self._events = events

        self._stdout: str = ""
        self._stderr: str = ""

        self._result: Optional[ProcessResult] = None
        self._iteration_exception: Optional[Exception] = None

    def __iter__(self):
        return self._handle_events()

    def _handle_events(
        self,
    ) -> Generator[
        Union[
            Tuple[Stdout, None, None],
            Tuple[None, Stderr, None],
            Tuple[None, None, PtyOutput],
        ],
        None,
        None,
    ]:
        for event in self._events:
            if event.event.HasField("data"):
                if event.event.data.stdout:
                    out = event.event.data.stdout.decode()
                    self._stdout += out
                    yield out, None, None
                if event.event.data.stderr:
                    out = event.event.data.stderr.decode()
                    self._stderr += out
                    yield None, out, None
                if event.event.data.pty:
                    yield None, None, event.event.data.pty
            if event.event.HasField("end"):
                self._result = ProcessResult(
                    stdout=self._stdout,
                    stderr=self._stderr,
                    exit_code=event.event.end.exit_code,
                    error=event.event.end.error,
                )

    def disconnect(self) -> None:
        """
        Disconnect from the process. It does not kill the process. It only stops receiving events from the process.
        """
        self._events.close()

    def wait(
        self,
        on_pty: Optional[Callable[[PtyOutput], None]] = None,
        on_stdout: Optional[Callable[[str], None]] = None,
        on_stderr: Optional[Callable[[str], None]] = None,
    ) -> ProcessResult:
        """
        Waits for the process to finish and returns the result.
        If the process exits with a non-zero exit code, it throws a `ProcessExitException`.

        :param on_pty: Callback for pty output
        :param on_stdout: Callback for stdout output
        :param on_stderr: Callback for stderr output
        :return: Process result
        """
        try:
            for stdout, stderr, pty in self:
                if stdout is not None and on_stdout:
                    on_stdout(stdout)
                elif stderr is not None and on_stderr:
                    on_stderr(stderr)
                elif pty is not None and on_pty:
                    on_pty(pty)
        except StopIteration:
            pass
        except Exception as e:
            self._iteration_exception = handle_rpc_exception(e)

        if self._iteration_exception:
            raise self._iteration_exception

        if self._result is None:
            raise Exception("Process ended without an end event")

        if self._result.exit_code != 0:
            raise ProcessExitException(
                stdout=self._stdout,
                stderr=self._stderr,
                exit_code=self._result.exit_code,
                error=self._result.error,
            )

        return self._result

    def kill(self) -> bool:
        """
        Kills the process.
        :return: Whether the process was killed successfully
        """
        return self._handle_kill()
