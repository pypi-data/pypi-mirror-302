import asyncio
import logging
from asyncio import Protocol, Transport, Future, Queue
from threading import Lock

from ..exceptions import ParseError
from ..messages import BaseMessage, parse_message

__all__ = [
    "OWNProtocol",
]

log = logging.getLogger("pyown.protocol")


class OWNProtocol(Protocol):
    _transport: Transport
    _lock: Lock

    def __init__(
            self,
            on_connection_start: Future[Transport],
            on_connection_end: Future[Exception | None],
    ):
        """
        Initialize the protocol.

        Args:
            on_connection_start (Future): The future to set when the connection starts.
            on_connection_end (Future): The future to set when the connection ends.
        """
        self._on_connection_start: Future[Transport] = on_connection_start
        self._on_connection_end: Future[Exception | None] = on_connection_end

        # The queue was chosen because it supports both synchronous and asynchronous functions
        self._messages_queue: Queue[BaseMessage] = asyncio.Queue()

        self._lock = Lock()

    def connection_made(self, transport: Transport):  # type: ignore[override]
        """
        Called when the socket is connected.
        """
        log.info(f"Connection made")
        self._transport = transport
        self._on_connection_start.set_result(transport)

    def connection_lost(self, exc: Exception | None):
        """
        Called when the connection is lost or closed.
        """
        if exc is not None:
            log.info(f"Connection lost with exception: {exc}")
        else:
            log.info(f"Connection lost")
        if exc is None:
            self._on_connection_end.set_result(None)
        else:
            self._on_connection_end.set_exception(exc)

    def data_received(self, raw: bytes):
        """
        Called when some data is received.

        The data argument is a bytes object containing the incoming data.
        It tries to parse the data and call the on_message_received for each message received.

        Args:
            raw (bytes): The incoming data

        Returns:
            None
        """
        # In OpenWebNet, the message is always written with ascii characters
        try:
            data = raw.decode("ascii").strip()
        except UnicodeDecodeError as e:
            log.warning(f"Received data not ascii: {raw.hex()}")
            raise e

        # Sometimes multiple messages can be sent in the same packet
        try:
            messages = [parse_message(msg + "##") for msg in data.split("##") if msg]
        except ParseError as e:
            log.warning(f"Received invalid message: {e.tags}")
            raise e

        # If there are no messages, return
        if not messages:
            return

        log.debug(f"Received messages: {messages}")

        # Call the on_message_received future
        for msg in messages:
            self._messages_queue.put_nowait(msg)

    def pause_writing(self):
        """
        Called when the transport's buffer goes over the high-water mark.
        """
        self._lock.acquire()
        log.debug("Paused writing")

    def resume_writing(self):
        """
        Called when the transport buffer drains below the low-water mark.
        """
        self._lock.release()
        log.debug("Resumed writing")

    async def send_message(self, msg: BaseMessage, delay: float = 0.1):
        """
        Send a message to the server.

        Args:
            msg (BaseMessage): The message to send
            delay (float): The delay to wait before sending the message.
            If the messages are sent too fast, certain servers will respond with invalid messages.
        """
        data = msg.bytes

        # block multiple messages from being sent at the same time
        while self._lock.locked():
            await asyncio.sleep(delay)

        self._transport.write(data)
        log.debug(f"Sent message: {msg}")

    async def receive_messages(self) -> BaseMessage:
        """
        Receive a list of messages from the server.

        Returns:
            list[BaseMessage]: a list of messages that were sent in the same packet.
        """
        messages = await self._messages_queue.get()
        return messages
