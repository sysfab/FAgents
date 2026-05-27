from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .messages import Message, MessageRole, MessageDict


class Conversation:
    def __init__(self, *messages: Message):
        self.messages: list[Message] = list(messages)

    def get_from(self, role: MessageRole) -> list[Message]:
        return [message for message in self.messages if message.role == role]

    def add(self, *messages: Message) -> None:
        self.messages.extend(messages)

    def clear(self) -> None:
        self.messages.clear()

    def to_dicts(self) -> list[MessageDict]:
        return [message.to_dict() for message in self.messages]

    def __len__(self) -> int:
        return len(self.messages)

    def __getitem__(self, index) -> Message:
        return self.messages[index]

    def __iter__(self):
        return iter(self.messages)

    def __repr__(self) -> str:
        return f"Conversation({self.messages!r})"
