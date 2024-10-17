from functools import wraps
from typing import Callable, Optional


def curry(fn: Optional[Callable] = None) -> Callable:
    """
    Transforms a function into a curried version.

    Args:
        fn : Callable, optional
            The function to be curried. If not provided, `curry` is used as a decorator.

    Returns:
        Callable
            A curried version of the original function.

    Examples:
        1. Using `curry` directly:

            >>> def add(a, b, c):
            ...     return a + b + c

            >>> curried_add = curry(add)
            >>> result = curried_add(1)(2)(3)  # returns 6

        2. Using `curry` as a decorator:

            >>> @curry
            ... def multiply(a, b):
            ...     return a * b

            >>> result = multiply(2)(3)  # returns 6
    """

    if fn is None:
        return lambda f: curry(f)

    @wraps(fn)
    def curried(*args):
        if len(args) >= fn.__code__.co_argcount:
            return fn(*args)
        return lambda *more_args: curried(*args, *more_args)

    return curried
