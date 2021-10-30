import inspect
from typing import Callable


def get_arg_names(fn: Callable) -> list[str]:
    return list(inspect.signature(fn).parameters.keys())

