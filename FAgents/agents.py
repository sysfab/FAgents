from dataclasses import dataclass

from typing import TYPE_CHECKING, Literal, Callable

if TYPE_CHECKING:
    from FAgents.providers import Provider, Runner

type ReasoningMode = Literal["none", "minimal", "low", "medium", "high", "xhigh"]
type VerbosityMode = Literal["low", "medium", "high"]


@dataclass
class Agent:
    Name: str
    Instructions: str
    Reasoning: ReasoningMode = "none"
    Verbosity: VerbosityMode = "medium"

    @classmethod
    def GetRunner(cls, provider: Provider) -> Runner:
        return provider.GetRunner(cls)


def tool(func: Callable) -> Callable:
    return func
