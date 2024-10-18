from __future__ import annotations

import abc
import copy
import re
from enum import StrEnum
from typing import Final, TypeVar, Pattern, AnyStr, Self, Any

from ..exceptions import ParseError, InvalidMessage
from ..tags import Who, Where

__all__ = [
    "MessageType",
    "BaseMessage",
    "GenericMessage",
    "parse_message",
]


class MessageType(StrEnum):
    ACK = "ACK"
    NACK = "NACK"
    NORMAL = "NORMAL"
    STATUS_REQUEST = "STATUS REQUEST"
    DIMENSION_REQUEST = "DIMENSION REQUEST"
    DIMENSION_WRITING = "DIMENSION WRITING"
    DIMENSION_RESPONSE = "DIMENSION RESPONSE"
    GENERIC = "GENERIC"


class BaseMessage(abc.ABC):
    _type: MessageType = MessageType.GENERIC  # Type of the message
    _tags: Any  # Contains the tags of the message

    prefix: Final[str] = "*"  # Prefix of the message
    suffix: Final[str] = "##"  # Suffix of the message
    separator: Final[str] = "*"  # Separator of the tags

    _regex: Pattern[str] = re.compile(r"^\*(?:([0-9]*)(?:#[0-9]*)*\*?)+##$")  # Regex pattern used to match the message

    @abc.abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        raise NotImplementedError

    def __str__(self) -> str:
        """
        Return the message as a string.
        Returns:
            str: The message
        """
        return self.message

    def __repr__(self) -> str:
        """
        Return the representation of the message.
        Returns:
            str: The representation
        """
        return f"<{self.__class__.__name__}: {','.join([str(tag) for tag in self._tags])}>"

    def __hash__(self) -> int:
        return hash((self._type, self._tags))

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return self._type == other._type and self._tags == other._tags
        return False

    def __ne__(self, other) -> bool:
        return not self.__eq__(other)

    @classmethod
    def pattern(cls) -> Pattern[str]:
        """
        Return the regex pattern used to match the message represented by the class.
        Returns:
            Pattern[str]: The regex pattern
        """
        return cls._regex

    @property
    def tags(self) -> tuple[str] | list[str]:
        """
        Return the tags of the message.
        The tags are the elements that compose the message, like the WHO, WHAT, WHERE, etc.

        Returns:
            list[StrEnum, str]: The tags of the message
        """
        # Return a new copy of the tags to avoid modifications
        return copy.deepcopy(self._tags)

    @property
    def type(self) -> MessageType:
        """
        Return the type of the message.
        Returns:
            MessageType: The type of the message
        """
        return self._type

    @property
    @abc.abstractmethod
    def message(self) -> str:
        """
        Return the message represented by the class.
        Returns:
            str: The message
        """
        raise NotImplementedError

    @property
    def bytes(self) -> bytes:
        return self.message.encode("ascii")

    @classmethod
    @abc.abstractmethod
    def parse(cls, tags: list[str]) -> BaseMessage:
        """Parse the tags of a message from the OpenWebNet bus."""
        raise NotImplementedError

    @property
    def who(self) -> Who | None:
        """Return the WHO tag of the message."""
        return None

    @property
    def where(self) -> Where | None:
        """Return the WHAT tag of the message."""
        return None


class GenericMessage(BaseMessage):
    def __init__(self, tags: list[str]):
        self._tags = tags

    @property
    def message(self) -> str:
        return f"*{'*'.join(self._tags)}##"

    @classmethod
    def parse(cls, tags: list[str]) -> Self:
        return cls(tags=tags)


def parse_message(message: str) -> BaseMessage:
    """
    Parse a message from the OpenWebNet bus.

    Args:
        message (str): The message to parse

    Returns:
        BaseMessage: The appropriate message class instance,
        GenericMessage if the message has an unknown WHO tag or its structure is unknown
    """
    if message.count(BaseMessage.suffix) != 1:
        raise InvalidMessage(message=message)

    message = message.strip()

    tags = message.removeprefix(BaseMessage.prefix).removesuffix(BaseMessage.suffix).split(BaseMessage.separator)

    # First of all, check if the message is valid
    if GenericMessage.pattern().match(message) is None:
        raise ParseError(tags=tags, message="Invalid message")

    for subclass in BaseMessage.__subclasses__():
        if subclass is GenericMessage:
            continue

        # noinspection PyUnresolvedReferences
        match = subclass.pattern().match(message)
        if match is not None:
            return subclass.parse(tags)

    # Default case
    return GenericMessage.parse(tags)
