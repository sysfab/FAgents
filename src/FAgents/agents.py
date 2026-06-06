from dataclasses import dataclass

from FAgents.tool import tool

from typing import TYPE_CHECKING, Literal, Any

if TYPE_CHECKING:
    from FAgents.providers import Provider, Runner


@dataclass
class Agent:
    """
    Object that represents agent, holds their tools

    Args:
        Name (str): Name of the agent
        Instructions (str): Instructions for the agent
        Reasoning (Literal["none", "minimal", "low", "medium", "high", "xhigh"]): Reasoning mode of an agent

    Attributes:
        Tools (list[tool]): Agent's tools

    Usage:
        ```py
        from FAgents import Agent, tool

        class MyAgent(Agent):
            Name = "My Agent"
            Instructions = "You are helpful assistant"

            @tool
            def some_tool(...) -> ...:
                \"\"\"
                This tool allows you to do something
                \"\"\"
                ...
        ```
    """

    Name: str
    Instructions: str = ""
    Reasoning: Literal["none", "minimal", "low", "medium", "high", "xhigh"] = "none"

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        cls.Tools: list[tool] = [
            value for value in vars(cls).values() if isinstance(value, tool)
        ]

    @classmethod
    def runner(cls, provider: Provider) -> Runner:
        """
        Get specific provider's runner for an agent

        Args:
            provider (Provider): Provider to get runner from

        Returns:
            Provider specific runner

        Usage:
            ```py
            from FAgents.providers import OpenAI

            # Define your agent

            runner = MyAgent.runner(
                provider=OpenAI(model="...", token=...)
            )
            ```
        """
        return provider.runner(cls)
