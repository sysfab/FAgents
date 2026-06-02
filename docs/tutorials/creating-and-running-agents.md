---
title: Creating and running agents
---
# Creating and running agents

## Creating your first agent

To create your agent you just need to inherit from the [Agent][agent_url] class:
```py
from FAgents import Agent

class MyAgent(Agent):
    Name = "Agent"
    Instructions = "You are helpful assistant"
```  

---

You can also give them tools to use:
```py
from FAgents import Agent, tool

class MyAgent(Agent):
    Name = "Agent"
    Instructions = "You are helpful assistant that can search wikipedia"

    @tool
    def search_wikipedia(query: str) -> str:
        """
        Returns information about any topic from wikipedia
        """
        return "..."
```
> Tools is just a python functions that agent can call by itself  
> Tip: Add docstrings and type anotations, because agent sees them


## Running agents

To run agents, you need to create a [Runner][runner_url] object. For that, we need to choose our provider first.  

In this example we'll use OpenAI one:
```py
from FAgents.providers import OpenAI

# ... define your agent ...

runner = MyAgent.runner(
    provider = OpenAI(
        model = "gpt-5.4",
        token = ... # Your openai token
    )
)
```

---

We created our runner. To use it, we need to have a message history to use.  
We'll use predefined one, you will learn how to create them properly in later tutorials.  

Then we can use it to run the agent like this:
```py
import asyncio

from FAgents.messages import Messages
from FAgents.message import User

# ... define your agent, create runner ...

async def main():
    result = await runner.Run(
        Messages(
            User("Hello!")
        )
    )

asyncio.run(main())
``` 

---

As result we'll get [RunResult][run_result_url] object, let's just print the last new message:
```py
print(str(result.Message))
# "Hello! What can i help you with?"
```

## Final code
```py
import asyncio

from FAgents import Agent, tool

from FAgents.providers import OpenAI

from FAgents.messages import Messages
from FAgents.message import User


class MyAgent(Agent):
    Name = "Agent"
    Instructions = "You are helpful assistant that can search wikipedia"

    @tool
    def search_wikipedia(query: str) -> str:
        """
        Returns information about any topic from wikipedia
        """
        return "..."


runner = MyAgent.runner(
    provider = OpenAI(
        model = "gpt-5.4",
        token = ... # Your openai token
    )
)


async def main():
    result = await runner.Run(
        Messages(
            User("Hello!")
        )
    )

    print(str(result.Message))

asyncio.run(main())
```

<!-- References -->
[agent_url]: ../api-reference/#FAgents.Agent
[runner_url]: ../api-reference/#FAgents.Runner
[run_result_url]: ../api-reference/#FAgents.RunResult