from abc import ABC, abstractmethod
from dataclasses import dataclass

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from FAgents import Agent, tool
    from FAgents.messages import Messages, MessagesItem


@dataclass
class RunResult:
    """
    Object that represents results of a run

    Attributes:
        Message (MessagesItem): Last new message
        NewMessages (Messages): New messages
        ProviderSpecific (Any): Provider specific run result
    """

    Message: MessagesItem
    NewMessages: Messages
    ProviderSpecific: Any = None

    def __repr__(self):
        return f"RunResult(Message={self.Message},NewMessages={self.NewMessages},ProviderSpecific={self.ProviderSpecific})"


class Runner(ABC):
    """
    Object that parses data to/from provider specific format and returns run results
    """

    @abstractmethod
    async def run(
        self, messages: Messages, tools: None | list[tool[Any, Any]] = None
    ) -> RunResult:
        """
        Runs the agent with provider specific settings

        Args:
            messages (Messages): Message history
            tools (None | list[tool[Any, Any]]): Run-specific tools

        Returns:
            Run result

        Usage:
            ```py
            runner = MyAgent.runner(...)

            # In async function:
            result = await runner.Run(
                Messages(
                    User("Hi"!)
                )
            )

            print(str(result.Message))
            ```
        """
        ...


class Provider(ABC):
    """
    Object that holds provider specific settings such as tokens, model name, etc
    """

    @abstractmethod
    def runner(self, agent: type[Agent]) -> Runner:
        """
        Args:
            agent (type[Agent]): Agent to return a runner for

        Returns:
            Runner for an agent
        """
        ...
