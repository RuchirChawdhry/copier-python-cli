"""Expected application failures, distinct from programming errors."""


class ApplicationError(ValueError):
    """A user-facing failure that should be reported without a traceback."""
