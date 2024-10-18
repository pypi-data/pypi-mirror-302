class ClientException(Exception):
    """Base exception for TurboFiles client."""

    pass


class CompressionFailedException(ClientException):
    """Raised when compression task fails."""

    pass


class MaxRetriesExceededException(ClientException):
    """Raised when max retries are exceeded while waiting for task completion."""

    pass
