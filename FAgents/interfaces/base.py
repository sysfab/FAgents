import logging

from abc import ABC, abstractmethod

from FAgents.config import Config
from FAgents.agents import FAgent, Conversation

import json
from abc import ABC, abstractmethod
from pathlib import Path


class FInterface(ABC):
    def __init__(
        self,
        agent: FAgent,
        agent_config: Config,
        conversations_path: str,
    ):
        self.log = logging.getLogger(f"{self.__class__.__name__}<{agent_config.Name}>")
        self.log.info(f"Setting up...")

        self.agent = agent
        self.agent_config = agent_config

        self.conversations_path = Path(conversations_path)
        self.conversations: dict[str, Conversation] = {}

    def get_conversation(self, conv_id: str) -> Conversation:
        if conv_id in self.conversations:
            return self.conversations[conv_id]

        conversation = self.load_conversation(conv_id)

        if conversation is None:
            conversation = Conversation(
                max_history=self.agent_config.Conversation.MaxHistory
            )
            self.save_conversation(conv_id, conversation)

        self.conversations[conv_id] = conversation
        return conversation

    def load_conversation(self, conv_id: str) -> Conversation | None:
        if not self.conversations_path.exists():
            return None

        with open(self.conversations_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        conv_data = data.get(conv_id)

        if conv_data is None:
            return None

        return Conversation(
            max_history=conv_data.get(
                "max_history", self.agent_config.Conversation.MaxHistory
            ),
            history=conv_data.get("history", []),
        )

    def save_conversation(
        self,
        conv_id: str,
        conversation: Conversation,
    ) -> None:
        data = {}

        if self.conversations_path.exists():
            with open(self.conversations_path, "r", encoding="utf-8") as f:
                data = json.load(f)

        data[conv_id] = {
            "max_history": conversation.max_history,
            "history": conversation.history,
        }

        self.conversations_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(self.conversations_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @abstractmethod
    async def start(self) -> None:
        pass
