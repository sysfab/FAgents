import inspect
from functools import wraps

from typing import Any, Protocol


class NamedCallable[**P, R](Protocol):
    __name__: str
    __doc__: str | None

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...


class tool[**P, R]:
    """
    Wraps a callable as a named, documented tool for the agent

    Args:
        func (NamedCallable): Wrapped function

    Attributes:
        Name (str): Name of the tool
        Description (str): Description of the tool
        Signature (inspect.Signature): Signature of the tool
        IsAwaitable (bool): Is tool awaitable?
    """

    def __init__(self, func: NamedCallable[P, R]) -> None:
        self._func = func
        self.Name: str = func.__name__
        self.Description: str = inspect.cleandoc(func.__doc__ or "")
        self.Signature: inspect.Signature = inspect.signature(func)  # type: ignore[arg-type]
        self.IsAwaitable: bool = (
            inspect.iscoroutinefunction(func)
            or inspect.isasyncgenfunction(func)
            or inspect.isawaitable(func)
        )
        wraps(func)(self)  # type: ignore[arg-type]

    @property
    def func(self) -> NamedCallable[P, R]:
        return self._func

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        return self._func(*args, **kwargs)

    def __get__(self, obj: Any, objtype: Any = None) -> "tool[P, R]":
        return self

    def __repr__(self) -> str:
        return f"Tool(name={self.Name!r}, sig={self.Signature})"
