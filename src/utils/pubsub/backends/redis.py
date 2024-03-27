import logging
import random
import string

from redis import asyncio as asyncio_redis

from .Backend import PubSubBackendAbstract
from ..event import Event

logger = logging.getLogger(__name__)


class RedisBackend(PubSubBackendAbstract):
    def __init__(self, url: str):
        self.url = url

    async def connect(self) -> None:
        self.redis = asyncio_redis.from_url(self.url)
        self.pubsub = self.redis.pubsub()
        # next line is required for redis - subscribe to any channel before
        # starting to listen to published messages
        dummy_channel = ''.join(random.choices(
            string.ascii_lowercase + string.digits, k=20))
        await self.pubsub.subscribe(dummy_channel)

    async def disconnect(self):
        await self.redis.aclose()

    async def ping(self):
        await self.pubsub.ping()

    async def publish(self, channel: str, message: str):
        await self.redis.publish(channel, message)

    async def subscribe(self, channel):
        await self.pubsub.subscribe(channel)

    async def unsubscribe(self, channel):
        await self.pubsub.unsubscribe(channel)

    async def get_next_event(self) -> Event:
        while True:
            try:
                # event = next(await self.pubsub.listen())
                response = await self.pubsub.get_message(ignore_subscribe_messages=True, timeout=None)
                if response and ("channel" in response) and (
                        "data" in response):
                    event = Event(
                        channel=response["channel"].decode("utf-8"),
                        message=response["data"].decode("utf-8"),
                    )
                    return event
            except Exception as e:
                logger.info("Error in pubsub redis backend get_next_event():")
                logger.info(e)
