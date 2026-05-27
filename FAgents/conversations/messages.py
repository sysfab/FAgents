from dataclasses import dataclass

from typing import TypedDict, Literal, Union, cast


type TextType = Literal["text"]


class TextDict(TypedDict):
    text: str
    type: TextType


@dataclass
class Text:
    text: str

    def to_dict(self) -> TextDict:
        return {"text": self.text, "type": "text"}

    @classmethod
    def from_dict(cls, t_dict: TextDict) -> Text:
        return cls(text=t_dict["text"])


type ImageFormat = Literal["png", "jpg", "webp"]
type ImageType = Literal["image"]


class ImageDict(TypedDict):
    data: str
    format: ImageFormat
    type: ImageType


@dataclass
class Image:
    data: str
    format: ImageFormat

    def to_dict(self) -> ImageDict:
        return {"data": self.data, "format": self.format, "type": "image"}

    @classmethod
    def from_dict(cls, i_dict: ImageDict) -> Image:
        return cls(data=i_dict["data"], format=i_dict["format"])


type MessageRole = Literal["system", "user", "assistant"]
type MessageContent = str | list[Text | Image]
type MessageDictContent = str | list[TextDict | ImageDict]


class MessageDict(TypedDict):
    role: MessageRole
    content: MessageDictContent


@dataclass
class Message:
    role: MessageRole
    content: MessageContent

    def to_dict(self) -> MessageDict:
        if isinstance(self.content, str):
            content = self.content
        else:
            content = [element.to_dict() for element in self.content]
        return {"role": self.role, "content": content}

    @classmethod
    def from_dict(cls, m_dict: MessageDict) -> Message:
        if isinstance(m_dict["content"], list):
            content = []
            for content_dict in m_dict["content"]:
                match content_dict["type"]:
                    case "text":
                        content.append(Text.from_dict(cast(TextDict, content_dict)))
                    case "image":
                        content.append(Image.from_dict(content_dict))

            return cls(role=m_dict["role"], content=content)
        else:
            return cls(role=m_dict["role"], content=m_dict["content"])


def System(content: MessageContent) -> Message:
    return Message("system", content)


def User(content: MessageContent) -> Message:
    return Message("user", content)


def Assistant(content: MessageContent) -> Message:
    return Message("assistant", content)
