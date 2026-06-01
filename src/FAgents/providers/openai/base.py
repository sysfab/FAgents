from FAgents import Messages, Agent
from FAgents.providers import Runner, RunResult, Provider

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

from .utils import (
    to_openai_tool,
    to_openai_input,
    from_openai_input,
)


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any
    from FAgents import tool


class OpenAIRunner(Runner):
    def __init__(self, provider: OpenAI, agent: type[Agent]):
        self.provider: OpenAI = provider
        self.agent: type[Agent] = agent

    async def run(self, messages: Messages, tools: None | list[tool[Any, Any]] = None):
        tools = tools or list()
        tools.extend(self.agent.Tools)

        result = await AgentsRunner.run(
            AgentsAgent(
                name=self.agent.Name,
                instructions=self.agent.Instructions,
                tools=[to_openai_tool(tool) for tool in tools],
                model=self.provider.model,
                model_settings=ModelSettings(
                    reasoning=Reasoning(effort=self.agent.Reasoning),
                    verbosity=self.agent.Verbosity,
                ),
            ),
            input=to_openai_input(messages),
            run_config=RunConfig(model_provider=self.provider.openai_provider),
        )

        new_messages = from_openai_input(
            [item.to_input_item() for item in result.new_items]
        )
        message = new_messages[-1]

        return RunResult(
            Message=message,
            NewMessages=new_messages,
            ProviderSpecific=result,
        )


class OpenAI(Provider):
    """
    OpenAI's Agents-SDK provider

    Args:
        model (str): Model to use
        token (str): Token to use
    """

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

    def runner(self, agent: type[Agent]) -> OpenAIRunner:
        return OpenAIRunner(self, agent)
