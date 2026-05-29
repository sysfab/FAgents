from FAgents import Message, Messages, MessagesItem, Agent
from FAgents.providers import Runner, RunResult, Provider

from openai import AsyncOpenAI
from openai.types.shared import Reasoning

from agents import (
    ModelSettings,
    OpenAIProvider,
    RunConfig,
    MessageOutputItem,
    ToolCallItem,
    ToolCallOutputItem,
    set_default_openai_key,
)

from agents import Agent as AgentsAgent
from agents import Runner as AgentsRunner

from .utils import (
    to_openai_tool,
    to_openai_input,
    openai_to_message,
    openai_to_tool_call,
    openai_to_tool_call_output,
)


from typing import TYPE_CHECKING, cast

if TYPE_CHECKING:
    from typing import Any, Callable
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

        new_messages = Messages()
        for message in result.new_items:
            new_message = None

            if message.type == "message_output_item":
                new_message = openai_to_message(cast(MessageOutputItem, message))
            elif message.type == "tool_call_item":
                new_message = openai_to_tool_call(cast(ToolCallItem, message))
            elif message.type == "tool_call_output_item":
                new_message = openai_to_tool_call_output(
                    cast(ToolCallOutputItem, message)
                )

            if new_message != None:
                new_messages.add(new_message)

        message = cast(Message, new_messages[-1])

        return RunResult(
            Message=message,
            NewMessages=new_messages,
            ProviderSpecific=result,
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

    def runner(self, agent: type[Agent]) -> OpenAIRunner:
        return OpenAIRunner(self, agent)
