from typing import List
import logging
import asyncio

from fastapi import FastAPI
from broadcaster import Broadcast

from helpers_classes.async_stream import AsyncStream

logger = logging.getLogger(__name__)

def get_broadcaster(broadcast_url: str) -> Broadcast:
    broadcast = Broadcast(broadcast_url)
    return broadcast

def enable_broadcaster(app: FastAPI, broadcast: Broadcast, broadcast_subscribers_async_tasks: List[asyncio.Task]) -> Broadcast:
    @app.on_event("startup")
    async def startup_event():
        await broadcast.connect()

    @app.on_event("shutdown")
    async def shutdown_event():
        # Wait max 5 seconds for broadcast subscribe tasks to complete before disconnecting broadcast
        # Ideally, on app shutdown, websocket connections will be forcibly closed by FastAPI,
        # the teardown code in src/socket_endpoints/main_socket/socket_channel_subscriptions_manager.py
        # will send websocket_closed event via async stream to all subscriber tasks which should end all of them
        # Below line 29 that awaits tasks to complete is only needed for the tests - where the app is shutting down and
        # broadcast is disconnected before all the subscriber tasks are ended, resulting in an error
        await asyncio.wait_for(asyncio.gather(*broadcast_subscribers_async_tasks), 5)
        await broadcast.disconnect()

async def assert_broadcaster_is_able_to_connect_to_backend(broadcast: Broadcast):
    try:
        await asyncio.wait_for(broadcast.connect(), 5)
        await broadcast.disconnect()
        logger.info("Test broadcast connection to backend established successfully")
    except Exception as e:
        logger.info("Error connecting to broadcast backend")
        raise e
