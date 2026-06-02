---
title: Managing history
---
# Managing history

## Messages

FAgents provides [Messages][messages_url] class to manage your message history.  

Let's create simple predefined history first:
```py
from FAgents.messages import Messages
from Fagents.message import User, Assistant

history = Messages(
    User("Hello!"),
    Assistant("Hello! How can i help you?")
)
```  
> Here we used [User][user_url] and [Assistant][assistant_url] helpers to define our history  
> You can also use [Message][message_url] directly, if you want

---

Now we can manipulate our history:
```py
# Add messages
history.add(
    User("What is capital of France?"),
    Assistant("Paris.")
)

# Extend from other history, for example, runner result
history.extend(result.NewMessages)

# Or.. just clear it
history.clear()
```
> Messages have similar functions to a list objects  


Or retrieve information:
```py
# Get history length
len(history)

# Get the last message
history[-1]

# Loop over history
for message in history:
    ...

# Get all messages from user
history.get_from('user')
```

## Using with the agents

Most common usecase of [Messages][messages_url] will look something like that:
```py
async def main():
    history = Messages()

    while True:
        history.add(
            User(input("Enter your message: "))
        )

        result = runner.Run(messages=history)
        history.extend(result.NewMessages)

        print(f"Assistant: {result.Message}")
```

<!-- References -->
[messages_url]: ../api-reference/#FAgents.Messages
[user_url]: ../api-reference/#FAgents.User
[assistant_url]: ../api-reference/#FAgents.Assistant
[message_url]: ../api-reference/#FAgents.Message