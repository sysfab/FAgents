from FAgents.message import Message, MessageRole, ToolCall, ToolCallOutput


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
