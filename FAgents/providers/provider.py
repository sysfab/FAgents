from abc import ABC, abstractmethod

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from FAgents.agents import Agent
    from FAgents.conversations import Conversation


class Runner(ABC):
    @abstractmethod
    async def Run(self, conversation: Conversation): ...


class Provider(ABC):
    @abstractmethod
    def GetRunner(self, agent: type[Agent]) -> Runner: ...
