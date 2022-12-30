from typing import Any
import asyncio
import logging

from ..event import Event

logger = logging.getLogger(__name__)

class InMemoryBackend:
    def __init__(self):
        self._published_events = asyncio.Queue()

    async def connect(self):
        pass

    async def disconnect(self):
        pass

    async def ping(self):
        pass

    async def publish(self, channel: str, message: Any):
        await self._published_events.put(Event(channel=channel, message=message))

    async def subscribe(self, channel: str):
        pass

    async def unsubscribe(self, channel: str):
        pass

    async def get_next_event(self) -> Event:
        event = await self._published_events.get()
        return event
