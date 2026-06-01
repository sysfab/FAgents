from dataclasses import dataclass

import base64
from pathlib import Path
import filetype

from typing import Literal


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
        return cls(url=i_dict["url"], format=i_dict["format"], detail=i_dict["detail"])

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
