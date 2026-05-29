from abc import ABC, abstractmethod
from dataclasses import dataclass


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Callable
    from FAgents.agents import Agent
    from FAgents.conversations import Message, Conversation


@dataclass
class RunResult:
    Message: Message
    Exception: Exception | None = None
    ProviderSpecific: Any = None


class Runner(ABC):
    @abstractmethod
    async def Run(
        self, conversation: Conversation, tools: None | list[Callable] = None
    ) -> RunResult: ...


class Provider(ABC):
    @abstractmethod
    def GetRunner(self, agent: type[Agent]) -> Runner: ...
