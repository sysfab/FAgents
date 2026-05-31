from abc import ABC, abstractmethod
from dataclasses import dataclass


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any
    from FAgents import Messages, MessagesItem, Agent, tool


@dataclass
class RunResult:
    Message: MessagesItem
    NewMessages: Messages
    ProviderSpecific: Any = None

    def __repr__(self):
        return f"RunResult(Message={self.Message},NewMessages={self.NewMessages},ProviderSpecific={self.ProviderSpecific})"


class Runner(ABC):
    @abstractmethod
    async def run(
        self, messages: Messages, tools: None | list[tool[Any, Any]] = None
    ) -> RunResult: ...


class Provider(ABC):
    @abstractmethod
    def runner(self, agent: type[Agent]) -> Runner: ...
