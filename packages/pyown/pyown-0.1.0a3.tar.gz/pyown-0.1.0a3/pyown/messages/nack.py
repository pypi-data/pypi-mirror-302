import re
from typing import Self, Pattern, AnyStr, Final

from .base import BaseMessage, MessageType
from ..exceptions import ParseError

__all__ = [
    "NACK",
]


class NACK(BaseMessage):
    """
    Represent a NACK message

    Syntax: *#*0##
    """
    _type: MessageType = MessageType.NACK
    _tags: tuple[str, str] = ("#", "0")

    _regex: Pattern[str] = re.compile(r"^\*#\*0##$")

    def __init__(self):
        pass

    @property
    def message(self) -> str:
        return "*#*0##"

    @classmethod
    def parse(cls, tags: list[str]) -> Self:
        """Parse the tags of a message from the OpenWebNet bus."""
        # the first tag bust be #
        if tags[0] != "#" and tags[1] != "0":
            raise ParseError(tags=tags, message="Invalid ACK message")

        return cls()
