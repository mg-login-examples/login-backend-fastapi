import asyncio
import logging
from asyncio import Queue
from random import randint
from typing import AsyncGenerator

from .event import Event

logger = logging.getLogger(__name__)


class Unsubscribed(Exception):
    pass


class Subscriber:
    def __init__(self, name: str | None = None):
        self._queue: Queue = asyncio.Queue()
        self._name = name if name else str(randint(100000, 999999))

    async def __aiter__(self) -> AsyncGenerator:
        logger.debug(f"Entering subscriber '{self._name}' events' asynchronous context")
        try:
            while True:
                event = await self.get()
                yield event
        except Unsubscribed:
            logger.debug(
                f"Exiting subscriber '{self._name}' events' asynchronous context"
            )
            pass

    async def exit_async_iter(self) -> None:
        logger.debug(
            f"Trigger exit for subscriber '{self._name}' events' asynchronous context"
        )
        await self._queue.put(None)

    async def get(self, timeout: float | None = None) -> Event:
        try:
            logger.debug(f"Wait to receive next event from queue {self._name}")
            item = await asyncio.wait_for(self._queue.get(), timeout=timeout)
            logger.debug(f"Subscriber received in queue {self._name} item {item}")
            if item is None:
                raise Unsubscribed()
            return item
        except asyncio.TimeoutError:
            raise TimeoutError() from None

    async def put(self, event: Event | None):
        await self._queue.put(event)

    async def __aenter__(self) -> "Subscriber":
        logger.debug(f"Entering subscriber '{self._name}'")
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        logger.debug(f"Exiting subscriber '{self._name}'")
        await self.exit_async_iter()
