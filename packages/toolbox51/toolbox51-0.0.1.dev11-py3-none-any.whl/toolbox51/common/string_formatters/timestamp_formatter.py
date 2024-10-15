__all__ = ["formatter"]

import functools
from typing import Any, Callable

def message(timestamp: float, message: Any) -> str:
    return f"{timestamp} | {message}"
def formatter(timestamp: float) -> Callable[[Any], str]:
    return functools.partial(message, timestamp)