from typing import Any


class Message:
    def __init__(self, role: str, content: Any):
        self.role = role
        self.content = content

    def to_dict(self) -> dict:
        return {"role": self.role, "content": self.content}

    def __str__(self):
        return f"Message<{self.role}|{self.content}>"

    def __repr__(self):
        return self.__str__()


def System(content: Any):
    return Message("system", content)


def User(content: Any):
    return Message("user", content)


def Assistant(content: Any):
    return Message("assistant", content)
