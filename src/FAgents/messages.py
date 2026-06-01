import base64
from pathlib import Path
import filetype
from dataclasses import dataclass

from typing import Literal, Any


@dataclass
class Text:
    """
    Object that represents text

    Attributes:
        text (str): Text
    """

    text: str

    def to_dict(self) -> dict:
        return {"text": self.text, "type": "text"}

    @classmethod
    def from_dict(cls, t_dict: dict) -> Text:
        return cls(text=t_dict["text"])

    def __str__(self) -> str:
        return self.text


@dataclass
class Image:
    """
    Object that represents image

    Attributes:
        url (str): Image URL
        format (str): MIME-type of an image
        detail (Literal["low", "high", "auto", "original"]): Detail level of an image
    """

    url: str
    format: str
    detail: Literal["low", "high", "auto", "original"] = "auto"

    def to_dict(self) -> dict:
        return {
            "type": "image",
            "url": self.url,
            "format": self.format,
            "detail": self.detail,
        }

    @classmethod
    def from_base64(cls, data: str, format: str, **kwargs) -> Image:
        url = f"data:{format};base64,{data}"
        return cls(url=url, format=format, **kwargs)

    @classmethod
    def from_file(cls, path: str | Path, **kwargs) -> Image:
        path = Path(path)
        mime = filetype.guess(path).mime
        data = base64.b64encode(path.read_bytes()).decode()
        return cls.from_base64(data=data, format=mime, **kwargs)

    @classmethod
    def from_dict(cls, i_dict: dict) -> Image:
        return cls(
            url=i_dict["url"], format=i_dict["format"], detail=i_dict.get("detail")
        )

    def __str__(self) -> str:
        return "[Image]"


@dataclass
class File:
    """
    Object that represents file

    Attributes:
        id (str | None): File ID
        url (str | None): File URL
        data (str | None): File data
        filename (str | None): File name
        detail (Literal["low", "high"]): Detail level of a file
    """

    id: str | None = None
    url: str | None = None
    data: str | None = None
    filename: str | None = None
    detail: Literal["low", "high"] = "high"

    def to_dict(self) -> dict:
        return {
            "type": "file",
            "id": self.id,
            "url": self.url,
            "data": self.data,
            "filename": self.filename,
            "detail": self.detail,
        }

    @classmethod
    def from_base64(cls, data: str, filename: str, **kwargs) -> File:
        return cls(data=data, filename=filename, **kwargs)

    @classmethod
    def from_file(cls, path: str | Path, **kwargs) -> File:
        path = Path(path)
        guess = filetype.guess(path)
        mime = guess.mime if guess is not None else "text/plain"
        raw = base64.b64encode(path.read_bytes()).decode()
        data = f"data:{mime};base64,{raw}"
        return cls.from_base64(data=data, filename=path.name, **kwargs)

    @classmethod
    def from_dict(cls, f_dict: dict) -> File:
        return cls(
            detail=f_dict["detail"],
            id=f_dict.get("id"),
            url=f_dict.get("url"),
            data=f_dict.get("data"),
            filename=f_dict.get("filename"),
        )

    def __str__(self) -> str:
        if self.filename is not None:
            return f"[File '{self.filename}']"
        else:
            return "[File]"


type MessageRole = Literal["user", "assistant", "system", "developer"]
"""Represents the role of a message sender in a chat conversation"""


@dataclass
class Message:
    """
    Object that represents message

    Attributes:
        role (MessageRole): Message role
        content (list[Text | Image | File]): Message content
    """

    role: MessageRole
    content: list[Text | Image | File]

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
    def _message(*content: MessageContent | str) -> Message:
        parts: MessageContent = []
        for c in content:
            if isinstance(c, str):
                parts.append(Text(c))
            elif isinstance(c, list):
                parts.extend(c)
            else:
                parts.append(c)
        return Message(role=role, content=parts)

    return _message


User = _RoleMessage("user")
Assistant = _RoleMessage("assistant")
System = _RoleMessage("system")
Developer = _RoleMessage("developer")


@dataclass
class ToolCall:
    """
    Object that represents tool call
    """

    arguments: str
    name: str
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
        call_id (str | None): Call ID of an output
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


type MessagesItem = Message | ToolCall | ToolCallOutput
"""Elements that Messages object can hold"""


class Messages:
    """
    Object that stores message history (includes messages, tool calls, etc)

    Args:
        *messages (MessagesItem): Messages to store initially
    """

    def __init__(self, *messages: MessagesItem):
        self.messages: list[MessagesItem] = list(messages)

    def get_from(self, role: MessageRole) -> list[Message]:
        """
        Returns all messages from specific role

        Args:
            role (MessageRole): Role to get messages from

        Returns:
            List of messages from this role
        """
        return [
            message
            for message in self.messages
            if isinstance(message, Message) and message.role == role
        ]

    def add(self, *messages: MessagesItem) -> None:
        """
        Add new messages to the end of the history

        Args:
            *messages (MessagesItem): Messages to add
        """
        self.messages.extend(messages)

    def extend(self, messages: Messages) -> None:
        """
        Add messages from another Messages object

        Args:
            messages (Messages): Messages to add
        """
        self.messages.extend(messages.messages)

    def clear(self) -> None:
        """
        Clear messages
        """
        self.messages.clear()

    def to_dicts(self) -> list[dict]:
        return [message.to_dict() for message in self.messages]

    def __len__(self) -> int:
        return len(self.messages)

    def __getitem__(self, index) -> MessagesItem:
        return self.messages[index]

    def __iter__(self):
        return iter(self.messages)

    def __repr__(self) -> str:
        return f"Messages({self.messages!r})"
