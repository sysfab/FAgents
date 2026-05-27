from __future__ import annotations

import logging

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

import json

from FAgents.config import Config


class Conversation:
    def __init__(
        self,
        max_history: int = 20,
        history: List[Dict[str, Any]] | None = None,
    ):
        self.max_history = max_history

        self.history: List[Dict[str, Any]] = history or []
        self.tools: List[Any] = []

        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history :]

    def add_message(self, role: str, content: str | dict) -> None:
        self.history.append(
            {
                "role": role,
                "content": content,
            }
        )

        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history :]

    def clear_history(self) -> None:
        self.history.clear()

    def add_tool(self, tool: Any) -> None:
        self.tools.append(tool)

    def remove_tool(self, tool: Any) -> None:
        self.tools.remove(tool)

    def clear_tools(self) -> None:
        self.tools.clear()

    def to_json(self) -> str:
        return json.dumps(
            {
                "max_history": self.max_history,
                "history": self.history,
            }
        )

    @classmethod
    def from_json(cls, data: str) -> "Conversation":
        payload = json.loads(data)

        return cls(
            max_history=payload.get("max_history", 20),
            history=payload.get("history", []),
        )

    def __len__(self) -> int:
        return len(self.history)

    def __iter__(self):
        return iter(self.history)

    def __repr__(self) -> str:
        return (
            f"Conversation("
            f"messages={len(self.history)}, "
            f"tools={len(self.tools)}, "
            f"max_history={self.max_history}"
            f")"
        )


class FAgent(ABC):
    """
    Base class for all FAgent providers.
    """

    def __init__(self, config: Config) -> None:
        self.log = logging.getLogger(f"{self.__class__.__name__}<{config.Name}>")
        self.log.info(f"Setting up...")

        self.agent = None
        self.config = config

    @abstractmethod
    async def run(self, conversation: Conversation, **kwargs: Any) -> Any:
        """
        Execute agent inference for a given conversation.
        """
        raise NotImplementedError
