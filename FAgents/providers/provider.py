from abc import ABC, abstractmethod

from FAgents.conversations import Conversation


class Runner(ABC):
    @abstractmethod
    async def Run(self, conversation: Conversation): ...


class Provider(ABC):
    @abstractmethod
    def Runner(self, agent) -> Runner: ...
