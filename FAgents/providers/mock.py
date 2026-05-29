from FAgents import Assistant, Agent
from FAgents.providers import Runner, RunResult, Provider

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Any, Callable
    from FAgents import Messages, tool


class MockRunner(Runner):
    def __init__(self, provider: Mock, agent: type[Agent]):
        self.provider: Mock = provider
        self.agent: type[Agent] = agent

    async def run(
        self, messages: Messages, tools: None | list[tool[Any, Any]] = None
    ) -> RunResult:
        return RunResult(
            NewMessages=Messages(Assistant("Hello world!")),
            Message=Assistant("Hello world!"),
        )


class Mock(Provider):
    def __init__(self):
        pass

    def runner(self, agent: type[Agent]) -> MockRunner:
        return MockRunner(self, agent)
