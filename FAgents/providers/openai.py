from .provider import Runner, Provider

from FAgents.agents import Agent

from openai import AsyncOpenAI
from openai.types.shared import Reasoning

from agents import (
    ModelSettings,
    OpenAIProvider,
    RunConfig,
    set_default_openai_key,
)
from agents import Agent as AgentsAgent
from agents import Runner as AgentsRunner


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from FAgents.conversations import Conversation


class OpenAIRunner(Runner):
    def __init__(self, provider: OpenAI, agent: type[Agent]):
        self.provider: OpenAI = provider
        self.agent: type[Agent] = agent

    async def Run(self, conversation: Conversation, tools=None):
        tools = tools or list()

        return await AgentsRunner.run(
            AgentsAgent(
                name=self.agent.Name,
                instructions=self.agent.Instructions,
                tools=tools,
                model=self.provider.model,
                model_settings=ModelSettings(
                    reasoning=Reasoning(effort=self.agent.Reasoning),
                    verbosity=self.agent.Verbosity,
                ),
            ),
            input=conversation.to_dicts(),
            run_config=RunConfig(model_provider=self.provider.openai_provider),
        )


class OpenAI(Provider):
    def __init__(self, model: str, token: str):
        self.model = model
        self.token = token

        set_default_openai_key(token)

        self.openai_client = AsyncOpenAI(
            api_key=self.token,
            default_headers={"Authorization": f"Bearer {self.token}"},
        )

        self.openai_provider = OpenAIProvider(
            openai_client=self.openai_client,
            use_responses_websocket=True,
            responses_websocket_options={
                "ping_interval": 20.0,
                "ping_timeout": 60.0,
            },
        )

    def GetRunner(self, agent: type[Agent]):
        return OpenAIRunner(self, agent)
