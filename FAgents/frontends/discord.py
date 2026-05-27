from .frontend import Frontend


class Discord(Frontend):
    def __init__(self, runner, token: str):
        self.runner = runner
        self.token = token

    async def Serve(self):
        pass
