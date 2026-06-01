# FAgents  
FAgents is a python agent orchestration framework built for ease of use and plug-and-play providers (OpenAI, Claude, Google, Deepseek, Local, etc) with one syntax.  

## Example code  
Simple TUI chat with the agent:
```py
import asyncio

from FAgents import Agent, tool
from FAgents.providers import OpenAI

from FAgents.messages import Messages
from Fagents.message import User


class A(Agent):
    Name = "Agent"
    Instructions = "You are helpful assistant that can search wikipedia"

    @tool
    def search_wikipedia(query: str) -> str:
        """
        Returns information about any topic from wikipedia
        """
        return "..."


async def main():
    runner = A.runner(
        provider=OpenAI(model="gpt-5.4-mini", token=...),
    )

    conv = Messages()
    while True:
        i = input("> ")

        conv.add(i)
        result = await runner.run(conv)
        print(str(result.Message))

        conv.extend(result.NewMessages)

asyncio.run(main())
```  