from dataclasses import dataclass
from enum import Enum

from e2b.envd.filesystem.filesystem_pb2 import EventType


class FilesystemEventType(Enum):
    """
    Enum representing the type of filesystem event.
    """

    CHMOD = "chmod"
    CREATE = "create"
    REMOVE = "remove"
    RENAME = "rename"
    WRITE = "write"


def map_event_type(event: EventType):
    if event == EventType.EVENT_TYPE_CHMOD:
        return FilesystemEventType.CHMOD
    elif event == EventType.EVENT_TYPE_CREATE:
        return FilesystemEventType.CREATE
    elif event == EventType.EVENT_TYPE_REMOVE:
        return FilesystemEventType.REMOVE
    elif event == EventType.EVENT_TYPE_RENAME:
        return FilesystemEventType.RENAME
    elif event == EventType.EVENT_TYPE_WRITE:
        return FilesystemEventType.WRITE


@dataclass
class FilesystemEvent:
    """
    Contains information about the filesystem event - the name of the file and the type of the event.
    """

    name: str
    type: FilesystemEventType
