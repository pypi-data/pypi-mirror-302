from io import TextIOBase
from typing import IO, Iterator, List, Literal, Optional, Union, overload

import e2b_connect
import httpcore
import httpx
from e2b.connection_config import (
    ConnectionConfig,
    Username,
    KEEPALIVE_PING_HEADER,
    KEEPALIVE_PING_INTERVAL_SEC,
)
from e2b.envd.api import ENVD_API_FILES_ROUTE, handle_envd_api_exception
from e2b.envd.filesystem import filesystem_connect, filesystem_pb2
from e2b.envd.rpc import authentication_header, handle_rpc_exception
from e2b.sandbox.filesystem.filesystem import EntryInfo, map_file_type
from e2b.sandbox_sync.filesystem.watch_handle import WatchHandle


class Filesystem:
    """
    Manager for interacting with the filesystem in the sandbox.
    """

    def __init__(
        self,
        envd_api_url: str,
        connection_config: ConnectionConfig,
        pool: httpcore.ConnectionPool,
        envd_api: httpx.Client,
    ) -> None:
        self._envd_api_url = envd_api_url
        self._connection_config = connection_config
        self._pool = pool
        self._envd_api = envd_api

        self._rpc = filesystem_connect.FilesystemClient(
            envd_api_url,
            # TODO: Fix and enable compression again — the headers compression is not solved for streaming.
            # compressor=e2b_connect.GzipCompressor,
            pool=pool,
            json=True,
        )

    @overload
    def read(
        self,
        path: str,
        format: Literal["text"] = "text",
        user: Username = "user",
        request_timeout: Optional[float] = None,
    ) -> str: ...

    @overload
    def read(
        self,
        path: str,
        format: Literal["bytes"],
        user: Username = "user",
        request_timeout: Optional[float] = None,
    ) -> bytearray: ...

    @overload
    def read(
        self,
        path: str,
        format: Literal["stream"],
        user: Username = "user",
        request_timeout: Optional[float] = None,
    ) -> Iterator[bytes]: ...

    def read(
        self,
        path: str,
        format: Literal["text", "bytes", "stream"] = "text",
        user: Username = "user",
        request_timeout: Optional[float] = None,
    ):
        """
        Reads a whole file content and returns it in requested format (text by default).

        :param path: Path to the file
        :param format: Format of the file content
        :param user: Run the operation as this user
        :param request_timeout: Timeout for the request
        :return File content in requested format
        """
        r = self._envd_api.get(
            ENVD_API_FILES_ROUTE,
            params={"path": path, "username": user},
            timeout=self._connection_config.get_request_timeout(request_timeout),
        )

        err = handle_envd_api_exception(r)
        if err:
            raise err

        if format == "text":
            return r.text
        elif format == "bytes":
            return bytearray(r.content)
        elif format == "stream":
            return r.iter_bytes()

    def write(
        self,
        path: str,
        data: Union[str, bytes, IO],
        user: Username = "user",
        request_timeout: Optional[float] = None,
    ) -> EntryInfo:
        """
        Writes content to a file on the path.
        When writing to a file that doesn't exist, the file will get created.
        When writing to a file that already exists, the file will get overwritten.
        When writing to a file that's in a directory that doesn't exist, the directory will get created.

        :param path: Path to the file
        :param data: Data to write to the file
        :param user: Run the operation as this user
        :param request_timeout: Timeout for the request
        :return: Information about the written file
        """
        if isinstance(data, TextIOBase):
            data = data.read().encode()

        r = self._envd_api.post(
            ENVD_API_FILES_ROUTE,
            files={"file": data},
            params={"path": path, "username": user},
            timeout=self._connection_config.get_request_timeout(request_timeout),
        )

        err = handle_envd_api_exception(r)
        if err:
            raise err

        files = r.json()

        if not isinstance(files, list) or len(files) == 0:
            raise Exception("Expected to receive information about written file")

        file = files[0]
        return EntryInfo(**file)

    def list(
        self,
        path: str,
        user: Username = "user",
        request_timeout: Optional[float] = None,
    ) -> List[EntryInfo]:
        """
        Lists entries in a directory.

        :param path: Path to the directory
        :param user: Run the operation as this user
        :param request_timeout: Timeout for the request
        :return: List of entries in the directory
        """
        try:
            res = self._rpc.list_dir(
                filesystem_pb2.ListDirRequest(path=path),
                request_timeout=self._connection_config.get_request_timeout(
                    request_timeout
                ),
                headers=authentication_header(user),
            )

            entries: List[EntryInfo] = []
            for entry in res.entries:
                event_type = map_file_type(entry.type)

                if event_type:
                    entries.append(
                        EntryInfo(name=entry.name, type=event_type, path=entry.path)
                    )

            return entries
        except Exception as e:
            raise handle_rpc_exception(e)

    def exists(
        self,
        path: str,
        user: Username = "user",
        request_timeout: Optional[float] = None,
    ) -> bool:
        """
        Checks if a file or a directory exists.

        :param path: Path to a file or a directory
        :param user Run the operation as this user
        :param request_timeout Timeout for the request
        """
        try:
            self._rpc.stat(
                filesystem_pb2.StatRequest(path=path),
                request_timeout=self._connection_config.get_request_timeout(
                    request_timeout
                ),
                headers=authentication_header(user),
            )
            return True

        except Exception as e:
            if isinstance(e, e2b_connect.ConnectException):
                if e.status == e2b_connect.Code.not_found:
                    return False
            raise handle_rpc_exception(e)

    def remove(
        self,
        path: str,
        user: Username = "user",
        request_timeout: Optional[float] = None,
    ) -> None:
        """
        Removes a file or a directory.
        :param path: Path to a file or a directory
        :param user: Run the operation as this user
        :param request_timeout: Timeout for the request
        """
        try:
            self._rpc.remove(
                filesystem_pb2.RemoveRequest(path=path),
                request_timeout=self._connection_config.get_request_timeout(
                    request_timeout
                ),
                headers=authentication_header(user),
            )
        except Exception as e:
            raise handle_rpc_exception(e)

    def rename(
        self,
        old_path: str,
        new_path: str,
        user: Username = "user",
        request_timeout: Optional[float] = None,
    ) -> EntryInfo:
        """
        Renames a file or directory from one path to another.

        :param old_path Path to the file or directory to move
        :param new_path Path to move the file or directory to
        :param user Run the operation as this user
        :param request_timeout Timeout for the request

        :return: Information about the renamed file or directory
        """
        try:
            r = self._rpc.move(
                filesystem_pb2.MoveRequest(
                    source=old_path,
                    destination=new_path,
                ),
                request_timeout=self._connection_config.get_request_timeout(
                    request_timeout
                ),
                headers=authentication_header(user),
            )

            return EntryInfo(
                name=r.entry.name,
                type=map_file_type(r.entry.type),
                path=r.entry.path,
            )
        except Exception as e:
            raise handle_rpc_exception(e)

    def make_dir(
        self,
        path: str,
        user: Username = "user",
        request_timeout: Optional[float] = None,
    ) -> bool:
        """
        Creates a new directory and all directories along the way if needed on the specified path.

        :param path: Path to a new directory. For example '/dirA/dirB' when creating 'dirB'.
        :param user: Run the operation as this user
        :param request_timeout: Timeout for the request
        :return: True if the directory was created, False if the directory already exists
        """
        try:
            self._rpc.make_dir(
                filesystem_pb2.MakeDirRequest(path=path),
                request_timeout=self._connection_config.get_request_timeout(
                    request_timeout
                ),
                headers=authentication_header(user),
            )

            return True
        except Exception as e:
            if isinstance(e, e2b_connect.ConnectException):
                if e.status == e2b_connect.Code.already_exists:
                    return False
            raise handle_rpc_exception(e)

    def watch_dir(
        self,
        path: str,
        user: Username = "user",
        request_timeout: Optional[float] = None,
    ) -> WatchHandle:
        """
        Watches directory for filesystem events.
        To get events, use the `get_new_events` method on the returned handle.

        :param path: Path to a directory that will be watched
        :param user: Run the operation as this user
        :param request_timeout: Timeout for the request
        :return: Watcher handle
        """
        try:
            r = self._rpc.create_watcher(
                filesystem_pb2.CreateWatcherRequest(path=path),
                request_timeout=self._connection_config.get_request_timeout(
                    request_timeout
                ),
                headers={
                    **authentication_header(user),
                    KEEPALIVE_PING_HEADER: str(KEEPALIVE_PING_INTERVAL_SEC),
                },
            )
        except Exception as e:
            raise handle_rpc_exception(e)

        return WatchHandle(self._rpc, r.watcher_id)
