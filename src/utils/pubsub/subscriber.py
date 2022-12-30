from typing import Optional, AsyncGenerator
import asyncio

from .event import Event

class Unsubscribed(Exception):
    pass

class Subscriber:
    def __init__(self):
        self._queue = asyncio.Queue()

    async def __aiter__(self) -> Optional[AsyncGenerator]:
        try:
            while True:
                event = await self.get()
                yield event
        except Unsubscribed:
            pass

    async def get(self) -> Event:
        item = await self._queue.get()
        if item is None:
            raise Unsubscribed()
        return item

    async def put(self, event: Event):
        await self._queue.put(event)

    async def exit_async_iter(self) -> None:
        await self._queue.put(None)
