from dataclasses import dataclass

from typing import TypedDict, Literal, Union


type TextType = Literal["text"]


class TextDict(TypedDict):
    text: str
    type: TextType


@dataclass
class Text:
    text: str
    type: TextType = "text"

    def to_dict(self) -> TextDict:
        return {"text": self.text, "type": self.type}


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
    type: ImageType = "image"

    def to_dict(self) -> ImageDict:
        return {"data": self.data, "format": self.format, "type": self.type}


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


def System(content: MessageContent) -> Message:
    return Message("system", content)


def User(content: MessageContent) -> Message:
    return Message("user", content)


def Assistant(content: MessageContent) -> Message:
    return Message("assistant", content)
