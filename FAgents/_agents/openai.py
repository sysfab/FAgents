import os
from typing import Any

from openai import AsyncOpenAI
from openai.types.shared import Reasoning

from agents import (
    Agent,
    ModelSettings,
    OpenAIProvider,
    RunConfig,
    Runner,
    set_default_openai_key,
)

from .base import FAgent, Conversation


class FOpenAI(FAgent):
    def __init__(self, token: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.token = token
        set_default_openai_key(token)

        self.openai_client = AsyncOpenAI(
            api_key=self.token,
            default_headers={"Authorization": f"Bearer {self.token}"},
        )

        self.provider = OpenAIProvider(
            openai_client=self.openai_client,
            use_responses_websocket=True,
            responses_websocket_options={
                "ping_interval": 20.0,
                "ping_timeout": 60.0,
            },
        )

    async def run(self, conversation: Conversation, **kwargs: Any) -> Any:
        return await Runner.run(
            Agent(
                name=self.config.Agent.Name,
                instructions=self.config.Agent.Instructions,
                tools=conversation.tools,
                model=self.config.Agent.Model,
                model_settings=ModelSettings(
                    reasoning=Reasoning(effort=self.config.Agent.Reasoning),
                    verbosity=self.config.Agent.Verbosity,
                ),
            ),
            conversation.history,
            run_config=RunConfig(model_provider=self.provider),
            **kwargs,
        )
