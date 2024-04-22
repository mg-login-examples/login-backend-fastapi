import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from utils.pubsub import utils as pubsub_utils
from utils.pubsub.pubsub import PubSub

logger = logging.getLogger(__name__)


def get_lifespan(pubsub: PubSub, pubsub_subscribers_async_tasks: list[asyncio.Task]):
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        logger.debug("app lifespan on start - start")
        await pubsub.connect()
        logger.debug("app lifespan on start - end")
        yield
        logger.debug("app lifespan on destroy - start")
        await pubsub_utils.pubsub_disconnect_gracefully(
            pubsub, pubsub_subscribers_async_tasks
        )
        logger.debug("app lifespan on destroy - end")

    return lifespan
