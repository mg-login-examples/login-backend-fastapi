from typing import Dict, Any
import asyncio
from contextlib import asynccontextmanager
import logging

from fastapi import Depends

from .subscriber import Subscriber
from .backends.in_memory import InMemoryBackend
from .backends.redis import RedisBackend

logger = logging.getLogger(__name__)


class PubSub:
    def __init__(self, backend_url: str = ""):
        if backend_url == "memory://":
            self._backend: InMemoryBackend | RedisBackend = InMemoryBackend()
        elif "redis://" in backend_url:
            self._backend = RedisBackend(backend_url)
        self._listener_task = None

        self._channel_to_subscribers: Dict[str, list[Subscriber]] = {}

    async def connect(self):
        try:
            await self._backend.connect()
        except Exception as e:
            logger.error(f"Error while trying to connect to pubsub backend:")
            raise e
        if not self._listener_task or self._listener_task.done:
            self._listener_task = asyncio.create_task(self._listener())

    async def ping(self):
        await self._backend.ping()

    async def disconnect(self):
        if self._listener_task.done():
            self._listener_task.result()
        else:
            self._listener_task.cancel()
        await self._backend.disconnect()

    async def publish(self, channel: str, message: Any) -> None:
        await self._backend.publish(channel, message)

    @asynccontextmanager
    async def subscribe(self, channel: str):
        try:
            await self._backend.subscribe(channel)
            async with Subscriber() as subscriber:
                if channel in self._channel_to_subscribers:
                    self._channel_to_subscribers[channel].append(subscriber)
                else:
                    self._channel_to_subscribers[channel] = [subscriber]
                yield subscriber
        except Exception as e:
            logger.error("Error in pubsub subscribe")
            raise e
        finally:
            if channel in self._channel_to_subscribers:
                self._channel_to_subscribers[channel].remove(subscriber)
            if not self._channel_to_subscribers.get(channel):
                del self._channel_to_subscribers[channel]
                await self._backend.unsubscribe(channel)

    async def _listener(self) -> None:
        while True:
            try:
                event = await self._backend.get_next_event()
                for subscriber in self._channel_to_subscribers.get(
                        event.channel, []):
                    await subscriber.put(event)
            except Exception as e:
                logger.error("Error in PubSub listener for backend events:")
                logger.error(e)
                logger.error(type(e))
                raise e

    def get_pubsub_as_fastapi_dependency(self):
        def get_self():
            return self
        return Depends(get_self)
