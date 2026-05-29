from dataclasses import dataclass

from typing import TypedDict, Literal, Union, cast, Any


@dataclass
class Text:
    text: str

    def to_dict(self) -> dict:
        return {"text": self.text, "type": "text"}

    @classmethod
    def from_dict(cls, t_dict: dict) -> Text:
        return cls(text=t_dict["text"])


type ImageFormat = Literal["png", "jpg", "webp"]


@dataclass
class Image:
    url: str
    format: ImageFormat | None = None
    detail: Literal["low", "high", "auto", "original"] | None = None

    def to_dict(self) -> dict:
        return {
            "type": "image",
            "url": self.url,
            "format": self.format,
            "detail": self.detail,
        }

    @classmethod
    def from_dict(cls, i_dict: dict) -> Image:
        return cls(
            url=i_dict["url"], format=i_dict.get("format"), detail=i_dict.get("detail")
        )


@dataclass
class File:
    detail: Literal["low", "high"]
    id: str | None = None
    url: str | None = None
    data: str | None = None
    filename: str | None = None

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
    def from_dict(cls, f_dict: dict) -> File:
        return cls(
            detail=f_dict["detail"],
            id=f_dict.get("id"),
            url=f_dict.get("url"),
            data=f_dict.get("data"),
            filename=f_dict.get("filename"),
        )


type MessageRole = Literal["user", "assistant", "system", "developer"]
type MessageContent = list[Text | Image | File]


@dataclass
class Message:
    role: MessageRole
    content: MessageContent

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
        return "".join([item.text for item in self.content if isinstance(item, Text)])


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
        return Message(role, parts)

    return _message


User = _RoleMessage("user")
Assistant = _RoleMessage("assistant")
System = _RoleMessage("system")
Developer = _RoleMessage("developer")


@dataclass
class ToolCall:
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


class Messages:
    def __init__(self, *messages: MessagesItem):
        self.messages: list[MessagesItem] = list(messages)

    def get_from(self, role: MessageRole) -> list[MessagesItem]:
        return [
            message
            for message in self.messages
            if isinstance(message, Message) and message.role == role
        ]

    def add(self, *messages: MessagesItem) -> None:
        self.messages.extend(messages)

    def extend(self, messages: Messages) -> None:
        self.messages.extend(messages.messages)

    def clear(self) -> None:
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
