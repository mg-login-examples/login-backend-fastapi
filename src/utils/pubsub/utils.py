from typing import List
import logging
import asyncio

from fastapi import FastAPI
from utils.pubsub.pubsub import PubSub

logger = logging.getLogger(__name__)

def get_pubsub(pubsub_url: str = "", redis_pass: str = None) -> PubSub:
    if  "redis" in pubsub_url and redis_pass:
        redis_url_split = pubsub_url.split("//")
        pubsub_url = f'{redis_url_split[0]}//:{redis_pass}@{redis_url_split[1]}'
    pubsub = PubSub(pubsub_url)
    return pubsub

def enable_pubsub(app: FastAPI, pubsub: PubSub, pubsub_subscribers_async_tasks: List[asyncio.Task]):
    @app.on_event("startup")
    async def startup_event():
        await pubsub.connect()

    @app.on_event("shutdown")
    async def shutdown_event():
        # Wait max 5 seconds for pubsub subscribe tasks to complete before disconnecting pubsub
        # Ideally, on app shutdown, websocket connections will be forcibly closed by FastAPI,
        # the teardown code in src/socket_endpoints/main_socket/socket_channel_subscriptions_manager.py
        # will send websocket_closed event via async stream to all subscriber tasks which should end all of them
        # Below here on line 28 awaiting tasks to complete before disconnecting pubsub is only needed for the tests
        # without line 28, the app is shutting down and pubsub is disconnected
        # before all the subscriber tasks are ended, resulting in an error
        await asyncio.wait_for(asyncio.gather(*pubsub_subscribers_async_tasks), 5)
        await pubsub.disconnect()

async def assert_pubsub_is_able_to_connect_to_backend(pubsub: PubSub):
    try:
        await asyncio.wait_for(pubsub.connect(), 5)
        await asyncio.wait_for(pubsub.ping(), 5)
        logger.info("Test pubsub connection to backend established successfully")
    except Exception as e:
        logger.info("Error connecting to pubsub backend")
        raise e
    finally:
        try:
            await pubsub.disconnect()
        except Exception as e:
            pass
