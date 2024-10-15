import asyncio
import inspect
from typing import (
    Optional,
    Callable,
    Any,
    AsyncGenerator,
    Union,
    Tuple,
    Coroutine,
)

from e2b.envd.rpc import handle_rpc_exception
from e2b.envd.process import process_pb2
from e2b.sandbox.process.process_handle import (
    ProcessExitException,
    ProcessResult,
    Stderr,
    Stdout,
    PtyOutput,
)
from e2b.sandbox_async.utilts import OutputHandler


class AsyncProcessHandle:
    """
    Class representing a process. It provides methods for waiting and killing the process.
    """

    @property
    def pid(self):
        """
        Get the process ID.
        """
        return self._pid

    @property
    def stdout(self):
        """
        Stdout of the process.
        """
        return self._stdout

    @property
    def stderr(self):
        """
        Stderr of the process.
        """
        return self._stderr

    @property
    def error(self):
        """
        Error message of the process. It is `None` if the process is still running.
        """
        if self._result is None:
            return None
        return self._result.error

    @property
    def exit_code(self):
        """
        Exit code of the process. It is `None` if the process is still running.
        """
        if self._result is None:
            return None
        return self._result.exit_code

    def __init__(
        self,
        pid: int,
        handle_kill: Callable[[], Coroutine[Any, Any, bool]],
        events: AsyncGenerator[
            Union[process_pb2.StartResponse, process_pb2.ConnectResponse], Any
        ],
        on_stdout: Optional[OutputHandler[Stdout]] = None,
        on_stderr: Optional[OutputHandler[Stderr]] = None,
        on_pty: Optional[OutputHandler[PtyOutput]] = None,
    ):
        self._pid = pid
        self._handle_kill = handle_kill
        self._events = events

        self._stdout: str = ""
        self._stderr: str = ""

        self._on_stdout = on_stdout
        self._on_stderr = on_stderr
        self._on_pty = on_pty

        self._result: Optional[ProcessResult] = None
        self._iteration_exception: Optional[Exception] = None

        self._wait = asyncio.create_task(self._handle_events())

    async def _iterate_events(
        self,
    ) -> AsyncGenerator[
        Union[
            Tuple[Stdout, None, None],
            Tuple[None, Stderr, None],
            Tuple[None, None, PtyOutput],
        ],
        None,
    ]:
        async for event in self._events:
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

    async def disconnect(self) -> None:
        """
        Disconnects from the process. It does not kill the process. It only stops receiving events from the process.
        """
        self._wait.cancel()
        # BUG: In Python 3.8 closing async generator can throw RuntimeError.
        # await self._events.aclose()

    async def _handle_events(self):
        try:
            async for stdout, stderr, pty in self._iterate_events():
                if stdout is not None and self._on_stdout:
                    cb = self._on_stdout(stdout)
                    if inspect.isawaitable(cb):
                        await cb
                elif stderr is not None and self._on_stderr:
                    cb = self._on_stderr(stderr)
                    if inspect.isawaitable(cb):
                        await cb
                elif pty is not None and self._on_pty:
                    cb = self._on_pty(pty)
                    if inspect.isawaitable(cb):
                        await cb
        except StopAsyncIteration:
            pass
        except Exception as e:
            self._iteration_exception = handle_rpc_exception(e)

    async def wait(self) -> ProcessResult:
        """
        Waits for the process to finish and returns the result.
        If the process exits with a non-zero exit code, it throws a `ProcessExitException`.

        :return: Process result
        """
        await self._wait
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

    async def kill(self) -> bool:
        """
        Kills the process.
        :return: Whether the process was killed successfully
        """
        await self._handle_kill()
