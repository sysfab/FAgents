from typing import Callable


class Agent:
    Name: str
    Instructions: str

    @classmethod
    def Runner(cls, provider):
        return provider.Runner(cls)


def tool(func: Callable):
    return func
