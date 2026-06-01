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
        *content (str | Text | Image | File): Message contents, strings will be converted into Text objects
        role (MessageRole): Message role

    Attributes:
        content (list[Text | Image | File]): Message contents
        role (MessageRole): Message role
    
    Usage:
        ```py
        Message(
            "Hello! Can you describe this image?",
            Image.from_file("image.png"),

            role='user'
        )
        ```
    """

    content: list[Text | Image | File]
    role: MessageRole

    def __init__(self, *content: str | Text | Image | File, role: MessageRole):
        self.content: list[Text | Image | File] = [
            Text(item) if isinstance(item, str) else item for item in content
        ]
        self.role: MessageRole = role

    def to_dict(self) -> dict:
        content = [element.to_dict() for element in self.content]
        return {"type": "message", "content": content, "role": self.role}

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

        return cls(*content, role=m_dict["role"])

    def __str__(self) -> str:
        return "".join([str(item) for item in self.content])


def _RoleMessage(role: MessageRole):
    def _message(*args, **kwargs) -> Message:
        return Message(*args, role=role, **kwargs)

    return _message


def User(*args, **kwargs) -> Message:
    """
    Helper function that outputs Message with the 'user' role

    Returns:
        (Message): Message from the 'user'
    
    Usage:
        ```py
        User(
            "Hello! Can you describe this image?",
            Image.from_file("image.png"),
        )
        ```
    """
    return Message(*args, role="user", **kwargs)


def Assistant(*args, **kwargs) -> Message:
    """
    Helper function that outputs Message with the 'assistant' role

    Returns:
        (Message): Message from the 'assistant'
    
    Usage:
        ```py
        Assistant("Sorry, i can't help you with that")
        ```
    """
    return Message(*args, role="assistant", **kwargs)


def System(*args, **kwargs) -> Message:
    """
    Helper function that outputs Message with the 'system' role

    Returns:
        (Message): Message from the 'system'
    
    Usage:
        ```py
        System("You are helpful assistant")
        ```
    """
    return Message(*args, role="system", **kwargs)


def Developer(*args, **kwargs) -> Message:
    """
    Helper function that outputs Message with the 'developer' role

    Returns:
        (Message): Message from the 'developer'
    
    Usage:
        ```py
        Developer("Do not answer in text, use `send_message` tool")
        ```
    """
    return Message(*args, role="developer", **kwargs)
