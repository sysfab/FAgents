from dataclasses import dataclass

from typing import TypedDict, Literal, Union, cast


class TextDict(TypedDict):
    type: Literal["text"]
    text: str


@dataclass
class Text:
    text: str

    def to_dict(self) -> TextDict:
        return {"text": self.text, "type": "text"}

    @classmethod
    def from_dict(cls, t_dict: TextDict) -> Text:
        return cls(text=t_dict["text"])


type ImageFormat = Literal["png", "jpg", "webp"]


class ImageDict(TypedDict):
    type: Literal["image"]
    url: str
    format: ImageFormat
    detail: Literal["low", "high"] | None


@dataclass
class Image:
    url: str
    format: ImageFormat
    detail: Literal["low", "high"] | None = None

    def to_dict(self) -> ImageDict:
        return {
            "type": "image",
            "url": self.url,
            "format": self.format,
            "detail": self.detail,
        }

    @classmethod
    def from_dict(cls, i_dict: ImageDict) -> Image:
        return cls(
            url=i_dict["url"], format=i_dict.get("format"), detail=i_dict.get("detail")
        )


class FileDict(TypedDict, total=False):
    type: Literal["file"]
    detail: Literal["low", "high"]
    url: str | None
    id: str | None
    data: str | None
    filename: str | None


@dataclass
class File:
    detail: Literal["low", "high"]
    id: str | None = None
    url: str | None = None
    data: str | None = None
    filename: str | None = None

    def to_dict(self) -> FileDict:
        return {
            "type": "file",
            "id": self.id,
            "url": self.url,
            "data": self.data,
            "filename": self.filename,
            "detail": self.detail,
        }

    @classmethod
    def from_dict(cls, f_dict: FileDict) -> File:
        return cls(
            detail=f_dict["detail"],
            id=f_dict.get("id"),
            url=f_dict.get("url"),
            data=f_dict.get("data"),
            filename=f_dict.get("filename"),
        )


type MessageRole = Literal["system", "user", "assistant"]
type MessageContent = list[Text | Image | File]
type MessageDictContent = list[TextDict | ImageDict | FileDict]


class MessageDict(TypedDict):
    role: MessageRole
    content: MessageDictContent


@dataclass
class Message:
    role: MessageRole
    content: MessageContent

    def to_dict(self) -> MessageDict:
        content = [element.to_dict() for element in self.content]
        return {"role": self.role, "content": content}

    @classmethod
    def from_dict(cls, m_dict: MessageDict) -> Message:
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


def System(content: MessageContent | str) -> Message:
    if isinstance(content, str):
        return Message("user", [Text(content)])
    return Message("system", content)


def User(content: MessageContent | str) -> Message:
    if isinstance(content, str):
        return Message("user", [Text(content)])
    return Message("user", content)


def Assistant(content: MessageContent | str) -> Message:
    if isinstance(content, str):
        return Message("user", [Text(content)])
    return Message("assistant", content)
