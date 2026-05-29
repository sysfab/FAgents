from abc import ABC, abstractmethod
from dataclasses import dataclass


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Callable
    from FAgents import Message, Messages, Agent, tool


@dataclass
class RunResult:
    Message: Message
    Exception: Exception | None = None
    ProviderSpecific: Any = None


class Runner(ABC):
    @abstractmethod
    async def run(
        self, messages: Messages, tools: None | list[tool[Any, Any]] = None
    ) -> RunResult: ...


class Provider(ABC):
    @abstractmethod
    def runner(self, agent: type[Agent]) -> Runner: ...
