from FAgents import Assistant, Agent
from FAgents.providers import Runner, RunResult, Provider

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any
    from FAgents import Messages, tool


class MockRunner(Runner):
    """
    Mock runner for test purposes
    """

    def __init__(self, provider: Mock, agent: type[Agent]):
        self.provider: Mock = provider
        self.agent: type[Agent] = agent

    async def run(
        self, messages: Messages, tools: None | list[tool[Any, Any]] = None
    ) -> RunResult:
        """
        Returns:
            Run result (Always 1 message from assistant with text `Hello world!`)
        """
        return RunResult(
            NewMessages=Messages(Assistant("Hello world!")),
            Message=Assistant("Hello world!"),
        )


class Mock(Provider):
    """
    Mock provider for test purposes
    """

    def __init__(self):
        pass

    def runner(self, agent: type[Agent]) -> MockRunner:
        return MockRunner(self, agent)
