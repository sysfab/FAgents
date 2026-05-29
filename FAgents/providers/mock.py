from FAgents.providers import Runner, RunResult, Provider
from FAgents.agents import Agent
from FAgents.conversations import Assistant

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Callable
    from FAgents.agents import Tool
    from FAgents.conversations import Conversation


class MockRunner(Runner):
    def __init__(self, provider: Mock, agent: type[Agent]):
        self.provider: Mock = provider
        self.agent: type[Agent] = agent

    async def Run(
        self, conversation: Conversation, tools: None | list[Tool[Any, Any]] = None
    ):
        return RunResult(Message=Assistant("Hello world!"))


class Mock(Provider):
    def __init__(self):
        pass

    def GetRunner(self, agent: type[Agent]) -> MockRunner:
        return MockRunner(self, agent)
