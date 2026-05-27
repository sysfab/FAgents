import logging

import discord

logging.getLogger("discord").setLevel(logging.ERROR)

from FAgents.config import Config
from FAgents.agents import FAgent

from .base import FInterface


class DiscordInterface(FInterface):
    def __init__(
        self, agent: FAgent, agent_config: Config, token: str, *args, **kwargs
    ):
        super().__init__(agent, agent_config, *args, **kwargs)
        self.config = agent_config.Interfaces.Discord

        self.token = token
        self.client = discord.Client(intents=discord.Intents.all())

        @self.client.event
        async def on_ready():
            self.log.info(f"Logged in as {self.client.user}")

            conversation = self.get_conversation("test")

    async def start(self):
        await self.client.start(self.token)
