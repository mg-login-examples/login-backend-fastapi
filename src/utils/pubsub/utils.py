import logging
import asyncio

from fastapi import FastAPI
from utils.pubsub.pubsub import PubSub

logger = logging.getLogger(__name__)


def get_pubsub(pubsub_url: str = "", redis_pass: str | None = None) -> PubSub:
    if "redis" in pubsub_url and redis_pass:
        redis_url_split = pubsub_url.split("//")
        pubsub_url = f"{redis_url_split[0]}//:{redis_pass}@{redis_url_split[1]}"
    pubsub = PubSub(pubsub_url)
    return pubsub


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


async def pubsub_disconnect_gracefully(
    pubsub: PubSub, pubsub_subscribers_async_tasks: list[asyncio.Task]
):
    # Wait max 5 seconds for pubsub subscribe tasks to complete before disconnecting pubsub
    # Ideally, on app shutdown, websocket connections will be forcibly closed by FastAPI,
    # the teardown code in backend/socket_endpoints/main_socket/socket_channel_subscriptions_manager.py
    # will send websocket_closed event via async stream to all subscriber tasks which should end all of them
    # Below here on line 40 awaiting tasks to complete before disconnecting pubsub is only needed for integration tests.
    # Without line 40, the app is shutting down and pubsub is disconnected
    # before all the subscriber tasks are ended, resulting in an error
    try:
        await asyncio.wait_for(asyncio.gather(*pubsub_subscribers_async_tasks), 5)
    except asyncio.TimeoutError:
        logger.error(
            "pubsub subscribers tasks did not end within 5 sec and were cancelled!"
        )
    await pubsub.disconnect()
