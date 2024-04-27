import asyncio
import logging
from asyncio import Task
from contextlib import asynccontextmanager
from typing import Any, Dict

from fastapi import Depends

from .backends.in_memory import InMemoryBackend
from .backends.redis import RedisBackend
from .subscriber import Subscriber

logger = logging.getLogger(__name__)


class PubSub:
    def __init__(self, backend_url: str = ""):
        if backend_url == "memory://":
            self._backend: InMemoryBackend | RedisBackend = InMemoryBackend()
        elif "redis://" in backend_url:
            self._backend = RedisBackend(backend_url)
        self._listener_task: Task | None = None

        self._channel_to_subscribers: Dict[str, list[Subscriber]] = {}

    async def connect(self):
        logger.debug("Pubsub trying to connect")
        try:
            await self._backend.connect()
            logger.info("Pubsub connected successfully")
        except Exception as e:
            logger.error(f"Error while trying to connect to pubsub backend:")
            raise e
        if not self._listener_task or self._listener_task.done():
            logger.debug("Pubsub creating _listener_task to receive backend events")
            self._listener_task = asyncio.create_task(self._listener())
            logger.info("Pubsub created _listener_task")

    async def ping(self):
        logger.debug("Pubsub try to ping backend")
        await self._backend.ping()

    async def disconnect(self):
        if self._listener_task:
            if self._listener_task.done():
                pass
                # self._listener_task.result() # FIXME gets stuck here in tests
            else:
                self._listener_task.cancel()
        await self._backend.disconnect()

    async def publish(self, channel: str, message: Any) -> None:
        await self._backend.publish(channel, message)

    @asynccontextmanager
    async def subscribe(self, channel: str, subscriber_name: str | None = None):
        subscriber_reference: Subscriber | None = None
        try:
            await self._backend.subscribe(channel)
            async with Subscriber(name=subscriber_name) as subscriber:
                subscriber_reference = subscriber
                logger.debug(f"Pubsub created subscriber {subscriber_name}")
                self._store_channel_subscriber(channel, subscriber_reference)
                yield subscriber
        except Exception as e:
            logger.error("Error in pubsub subscribe")
            raise e
        finally:
            logger.debug(f"Pubsub handle subscriber exit for channel {channel}")
            self._remove_channel_subscriber(channel, subscriber_reference)
            await self._backend_unsubscribe_from_channel_if_no_subscribers(channel)

    async def _listener(self) -> None:
        logger.debug("Pubsub start listening to backend events - infinite loop")
        while True:
            try:
                # logger.debug("Pubsub start listening for next event")
                event = await self._backend.get_next_event()
                # logger.debug(f"Pubsub listener received next event {event}")
                for subscriber in self._channel_to_subscribers.get(event.channel, []):
                    await subscriber.put(event)
            except Exception as e:
                logger.error("Error in PubSub listener for backend events:")
                logger.error(e)
                raise e

    def _store_channel_subscriber(self, channel: str, subscriber: Subscriber):
        if channel in self._channel_to_subscribers:
            self._channel_to_subscribers[channel].append(subscriber)
        else:
            self._channel_to_subscribers[channel] = [subscriber]

    def _remove_channel_subscriber(self, channel: str, subscriber: Subscriber | None):
        if (
            subscriber
            and channel in self._channel_to_subscribers
            and subscriber in self._channel_to_subscribers[channel]
        ):
            self._channel_to_subscribers[channel].remove(subscriber)

    async def _backend_unsubscribe_from_channel_if_no_subscribers(self, channel: str):
        if not self._channel_to_subscribers.get(channel):
            del self._channel_to_subscribers[channel]
            await self._backend.unsubscribe(channel)

    def get_pubsub_as_fastapi_dependency(self):
        def get_self():
            return self

        return Depends(get_self)
