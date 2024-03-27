import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from utils.pubsub.pubsub import PubSub
from utils.pubsub import utils as pubsub_utils

logger = logging.getLogger(__name__)


def get_lifespan(pubsub: PubSub,
                 pubsub_subscribers_async_tasks: list[asyncio.Task]):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        await pubsub.connect()
        yield
        await pubsub_utils.pubsub_disconnect_gracefully(pubsub, pubsub_subscribers_async_tasks)
