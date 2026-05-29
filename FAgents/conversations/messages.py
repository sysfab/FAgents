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


@dataclass
class Image:
    url: str
    format: ImageFormat

    def to_dict(self) -> ImageDict:
        return {"url": self.url, "format": self.format, "type": "image"}

    @classmethod
    def from_dict(cls, i_dict: ImageDict) -> Image:
        return cls(url=i_dict["url"], format=i_dict["format"])


class FileDict(TypedDict):
    type: Literal["input_file"]
    file_id: str | None
    file_url: str | None
    file_data: str | None
    filename: str | None
    detail: Literal["low", "high"] | None


@dataclass
class File:
    file_id: str | None = None
    file_url: str | None = None
    file_data: str | None = None
    filename: str | None = None
    detail: Literal["low", "high"] | None = None

    def to_dict(self) -> FileDict:
        return {
            "type": "input_file",
            "file_id": self.file_id,
            "file_url": self.file_url,
            "file_data": self.file_data,
            "filename": self.filename,
            "detail": self.detail,
        }

    @classmethod
    def from_dict(cls, f_dict: FileDict) -> File:
        return cls(
            file_id=f_dict.get("file_id"),
            file_url=f_dict.get("file_url"),
            file_data=f_dict.get("file_data"),
            filename=f_dict.get("filename"),
            detail=f_dict.get("detail"),
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
