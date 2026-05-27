from .provider import Provider, Runner

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


class OpenAIRunner(Runner):
    def __init__(self, provider, agent):
        self.provider = provider
        self.agent = agent

    async def Run(self, conversation, tools=None):
        tools = tools or list()

        return await Runner.run(
            Agent(
                name=self.agent.Name,
                instructions=self.agent.Instructions,
                tools=tools,
                model=self.provider.model,
                model_settings=ModelSettings(
                    reasoning=Reasoning(effort=self.agent.Reasoning),
                    verbosity=self.agent.Verbosity,
                ),
            ),
            conversation.to_dict(),
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

    def Runner(self, agent):
        return OpenAIRunner(self, agent)
