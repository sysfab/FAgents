from dataclasses import dataclass, field
from functools import wraps
import inspect

from typing import TYPE_CHECKING, overload

if TYPE_CHECKING:
    from typing import Literal, Callable, ClassVar, Any
    from FAgents.providers import Provider, Runner

type ReasoningMode = Literal["none", "minimal", "low", "medium", "high", "xhigh"]
type VerbosityMode = Literal["low", "medium", "high"]


@dataclass
class Agent:
    Name: str
    Instructions: str
    Reasoning: ReasoningMode = "none"
    Verbosity: VerbosityMode = "medium"

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls.Tools = [value for value in vars(cls).values() if isinstance(value, Tool)]

    @classmethod
    def GetRunner(cls, provider: "Provider") -> "Runner":
        return provider.GetRunner(cls)


from typing import Protocol


class NamedCallable[**P, R](Protocol):
    __name__: str
    __doc__: str | None

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...


class Tool[**P, R]:
    """Wraps a callable as a named, documented tool."""

    def __init__(self, func: NamedCallable[P, R]) -> None:
        self._func = func
        self.Name: str = func.__name__
        self.Description: str = inspect.cleandoc(func.__doc__ or "")
        self.Signature: inspect.Signature = inspect.signature(func)  # type: ignore[arg-type]
        self.IsAwaitable = (
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

    def __get__(self, obj: Any, objtype: Any = None) -> "Tool[P, R]":
        return self

    def __repr__(self) -> str:
        return f"Tool(name={self.Name!r}, sig={self.Signature})"
