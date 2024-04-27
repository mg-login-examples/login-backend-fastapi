import asyncio
import logging
import random
import string

from redis import asyncio as asyncio_redis

from ..event import Event
from .Backend import PubSubBackendAbstract

logger = logging.getLogger(__name__)


class RedisBackend(PubSubBackendAbstract):
    def __init__(self, url: str):
        self.url = url
        self._pubsub_connected = False

    async def connect(self) -> None:
        if self._pubsub_connected:
            logger.debug("PubSub Redis backend is already connected")
            return
        logger.debug("PubSub backend RedisBackend trying to connect")
        try:
            self.redis = asyncio_redis.from_url(self.url)
            self.pubsub = self.redis.pubsub()
            # next line is required for redis - subscribe to any channel before
            # starting to listen to published messages
            dummy_channel = "".join(
                random.choices(string.ascii_lowercase + string.digits, k=20)
            )
            await self.pubsub.subscribe(dummy_channel)
            self._pubsub_connected = True
            logger.debug("PubSub backend RedisBackend connected successfully")
        except Exception as e:
            logger.error("Error in pubsub backend RedisBackend connect")
            logger.error(e)
            raise e

    async def disconnect(self):
        logger.debug("PubSub RedisBackend trying to disconnect")
        if hasattr(self, "redis") and self.redis:
            await self.redis.aclose()
        self._pubsub_connected = False
        logger.debug("PubSub RedisBackend disconnected successfully")

    async def ping(self):
        if not hasattr(self, "pubsub") or not self.pubsub:
            await self.connect()
        await self.pubsub.ping()

    async def publish(self, channel: str, message: str):
        if not hasattr(self, "pubsub") or not self.pubsub:
            await self.connect()
        # logger.debug(f"Publish message: {message} to channel {channel}")
        await self.redis.publish(channel, message)
        # logger.debug(f"Published message: {message} to channel {channel}")

    async def subscribe(self, channel):
        logger.debug(f"PubSub RedisBackend trying to subscribe to channel {channel}")
        if not hasattr(self, "pubsub") or not self.pubsub:
            await self.connect()
        try:
            await self.pubsub.subscribe(channel)
            logger.debug(
                f"PubSub RedisBackend subscribed successfully to channel '{channel}'"
            )
        except Exception as e:
            logger.error(
                f"Error when RedisBackend trying to subscribe to channel '{channel}'"
            )
            logger.error(e)
            raise e

    async def unsubscribe(self, channel):
        logger.debug(
            f"PubSub RedisBackend trying to unsubscribe from channel '{channel}'"
        )
        if not hasattr(self, "pubsub") or not self.pubsub:
            await self.connect()
        await self.pubsub.unsubscribe(channel)
        logger.debug(
            f"PubSub RedisBackend unsubscribed successfully from channel '{channel}'"
        )

    async def get_next_event(self) -> Event:
        while True:
            if not hasattr(self, "pubsub") or not self.pubsub:
                await self.connect()
            try:
                # event = next(await self.pubsub.listen())
                # logger.debug(
                #     f"Redis start wait for next event at self.pubsub.get_message"
                # )
                response = await self.pubsub.get_message(
                    ignore_subscribe_messages=True, timeout=None
                )
                # logger.debug(
                #     f"Redis received next event at self.pubsub.get_message {response}"
                # )
                if response and ("channel" in response) and ("data" in response):
                    event = Event(
                        channel=response["channel"].decode("utf-8"),
                        message=response["data"].decode("utf-8"),
                    )
                    # logger.debug(f"Redis received event message: {event.message}")
                    return event
            except Exception as e:
                logger.error("Error in pubsub redis backend get_next_event():")
                logger.error(e)
                await asyncio.sleep(0.1)  # To avoid infinite blocking loop
