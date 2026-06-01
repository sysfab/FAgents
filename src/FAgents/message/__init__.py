from dataclasses import dataclass

from .content import Text, Image, File

from typing import Literal, Any


type MessageRole = Literal["user", "assistant", "system", "developer"]
"""Represents the role of a message sender in a chat conversation"""


@dataclass
class ToolCall:
    """
    Object that represents tool call

    Attributes:
        name (str): Called function name
        arguments (str): Called function arguments
        status (str): Status of a tool call
        id (str):
        call_id (str | None): Tool call ID
    """

    name: str
    arguments: str
    status: str
    id: str
    call_id: str | None

    def to_dict(self) -> dict:
        return {
            "type": "tool_call",
            "arguments": self.arguments,
            "name": self.name,
            "status": self.status,
            "id": self.id,
            "call_id": self.call_id,
        }

    @classmethod
    def from_dict(cls, tc_dict: dict) -> ToolCall:
        return cls(
            arguments=tc_dict["arguments"],
            name=tc_dict["name"],
            status=tc_dict["status"],
            id=tc_dict["id"],
            call_id=tc_dict.get("call_id"),
        )


@dataclass
class ToolCallOutput:
    """
    Object that represents tool call output

    Attributes:
        output (Any): Output
        call_id (str | None): Tool Call ID
    """

    output: Any
    call_id: str | None

    def to_dict(self) -> dict:
        return {
            "type": "tool_call_output",
            "output": self.output,
            "call_id": self.call_id,
        }

    @classmethod
    def from_dict(cls, tco_dict: dict) -> ToolCallOutput:
        return cls(
            output=tco_dict["output"],
            call_id=tco_dict["call_id"],
        )


@dataclass
class Message:
    """
    Object that represents message

    Args:
        role (MessageRole): Message role
        content (list[str | Text | Image | File]): Message content, strings will be converted into Text objects

    Attributes:
        role (MessageRole): Message role
        content (list[Text | Image | File]): Message content
    """

    role: MessageRole
    content: list[Text | Image | File]

    def __init__(self, role: MessageRole, content: list[str | Text | Image | File]):
        self.role: MessageRole = role
        self.content: list[Text | Image | File] = [
            Text(item) if isinstance(item, str) else item for item in content
        ]

    def to_dict(self) -> dict:
        content = [element.to_dict() for element in self.content]
        return {"type": "message", "role": self.role, "content": content}

    @classmethod
    def from_dict(cls, m_dict: dict) -> Message:
        content = []
        for content_dict in m_dict["content"]:
            match content_dict["type"]:
                case "text":
                    content.append(Text.from_dict(content_dict))
                case "image":
                    content.append(Image.from_dict(content_dict))
                case "file":
                    content.append(File.from_dict(content_dict))

        return cls(role=m_dict["role"], content=content)

    def __str__(self) -> str:
        return "".join([str(item) for item in self.content])


def _RoleMessage(role: MessageRole):
    def _message(*args, **kwargs) -> Message:
        return Message(role=role, *args, **kwargs)

    return _message


def User(*args, **kwargs) -> Message:
    """
    Helper function that outputs Message with the 'user' role

    Returns:
        (Message): Message from the 'user'
    """
    return Message(role="user", *args, **kwargs)


def Assistant(*args, **kwargs) -> Message:
    """
    Helper function that outputs Message with the 'assistant' role

    Returns:
        (Message): Message from the 'assistant'
    """
    return Message(role="assistant", *args, **kwargs)


def System(*args, **kwargs) -> Message:
    """
    Helper function that outputs Message with the 'system' role

    Returns:
        (Message): Message from the 'system'
    """
    return Message(role="system", *args, **kwargs)


def Developer(*args, **kwargs) -> Message:
    """
    Helper function that outputs Message with the 'developer' role

    Returns:
        (Message): Message from the 'developer'
    """
    return Message(role="developer", *args, **kwargs)
