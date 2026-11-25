"""Optional function-level instrumentation using the configured Loguru logger."""

from collections.abc import Callable
from functools import wraps
from time import perf_counter

from loguru import logger


def log_call[**P, R](function: Callable[P, R]) -> Callable[P, R]:
    """Log a synchronous function's entry, duration and failure without logging its data."""
    name = function.__qualname__

    @wraps(function)
    def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
        started = perf_counter()
        logger.opt(depth=1).debug("Entering {}", name)
        try:
            result = function(*args, **kwargs)
        except Exception as error:
            logger.opt(depth=1).error(
                "Failed {} in {:.3f}s ({})", name, perf_counter() - started, type(error).__name__
            )
            raise
        logger.opt(depth=1).debug("Finished {} in {:.3f}s", name, perf_counter() - started)
        return result

    return wrapped
