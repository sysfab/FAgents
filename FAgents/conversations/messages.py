from typing import TypedDict, Literal, Union

type MessageRole = Literal["system", "user", "assistant"]
type MessageContent = str


class MessageDict(TypedDict):
    role: MessageRole
    content: MessageContent


class Message:
    def __init__(self, role: MessageRole, content: MessageContent):
        self.role: MessageRole = role
        self.content: MessageContent = content

    def to_dict(self) -> MessageDict:
        return {"role": self.role, "content": self.content}

    def __str__(self):
        return str(self.content)

    def __repr__(self):
        return f"Message<{self.role}|{self.content}>"


def System(content: MessageContent) -> Message:
    return Message("system", content)


def User(content: MessageContent) -> Message:
    return Message("user", content)


def Assistant(content: MessageContent) -> Message:
    return Message("assistant", content)
