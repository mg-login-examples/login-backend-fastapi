from typing import AsyncGenerator
import asyncio
from asyncio import Queue

from .event import Event


class Unsubscribed(Exception):
    pass


class Subscriber:
    def __init__(self):
        self._queue: Queue = asyncio.Queue()

    async def __aiter__(self) -> AsyncGenerator:
        try:
            while True:
                event = await self.get()
                yield event
        except Unsubscribed:
            pass

    async def exit_async_iter(self) -> None:
        await self._queue.put(None)

    async def get(self, timeout: float | None = None) -> Event:
        try:
            item = await asyncio.wait_for(self._queue.get(), timeout=timeout)
            if item is None:
                raise Unsubscribed()
            return item
        except asyncio.TimeoutError:
            raise TimeoutError() from None

    async def put(self, event: Event | None):
        await self._queue.put(event)

    async def __aenter__(self) -> 'Subscriber':
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> None:
        await self.exit_async_iter()
