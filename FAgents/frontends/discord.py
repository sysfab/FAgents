from .frontend import Frontend


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from FAgents.providers import Runner


class Discord(Frontend):
    def __init__(self, runner: Runner, token: str):
        self.runner: Runner = runner
        self.token: str = token

    async def Serve(self) -> None:
        pass
