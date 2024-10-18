from ._sync.client import SyncClient as Client
from ._async.client import AsyncClient
from .exceptions import (
    ClientException,
    CompressionFailedException,
    MaxRetriesExceededException,
)

__all__ = [
    "Client",
    "AsyncClient",
    "ClientException",
    "CompressionFailedException",
    "MaxRetriesExceededException",
]
__version__ = "0.1.0"
