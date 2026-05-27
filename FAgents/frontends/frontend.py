from abc import ABC, abstractmethod


class Frontend(ABC):
    @abstractmethod
    async def Serve(self): ...
