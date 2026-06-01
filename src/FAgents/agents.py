from dataclasses import dataclass
from functools import wraps
import inspect

from typing import TYPE_CHECKING, Literal, Any, Protocol

if TYPE_CHECKING:
    from FAgents.providers import Provider, Runner


@dataclass
class Agent:
    """
    Object that represents agent, holds their tools

    Args:
        Name (str): Name of the agent
        Instructions (str): Instructions for the agent
        Reasoning (Literal["none", "minimal", "low", "medium", "high", "xhigh"]): Reasoning mode of an agent
        Verbosity (Literal["low", "medium", "high"]): Verbosity of an agent

    Attributes:
        Tools (list[tool]): Agent's tools
    """

    Name: str
    Instructions: str = ""
    Reasoning: Literal["none", "minimal", "low", "medium", "high", "xhigh"] = "none"
    Verbosity: Literal["low", "medium", "high"] = "medium"

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls.Tools: list[tool] = [
            value for value in vars(cls).values() if isinstance(value, tool)
        ]

    @classmethod
    def runner(cls, provider: Provider) -> Runner:
        """
        Get specific provider's runner for an agent

        Args:
            provider (Provider): Provider to get runner from

        Returns:
            Provider specific runner
        """
        return provider.runner(cls)


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
