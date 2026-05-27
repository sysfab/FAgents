from typing import Any
from dataclasses import dataclass

from .base import FAgent, Conversation


@dataclass
class FakeResponse:
    final_result: str = "test"


class FTest(FAgent):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    async def run(self, conversation: Conversation, **kwargs: Any) -> Any:
        return FakeResponse()
