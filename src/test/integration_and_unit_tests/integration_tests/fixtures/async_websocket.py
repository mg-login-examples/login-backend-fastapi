import logging
from typing import AsyncIterator

import httpx
import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient
from httpx_ws import AsyncWebSocketSession, aconnect_ws
from httpx_ws.transport import ASGIWebSocketTransport

logger = logging.getLogger(__name__)


@pytest.fixture
async def async_test_client_for_websocket(app: FastAPI) -> AsyncIterator[AsyncClient]:
    logger.debug("Create fixture async_test_client_for_websocket")
    async with LifespanManager(app):
        async with httpx.AsyncClient(
            transport=ASGIWebSocketTransport(app), base_url="http://testserver"
        ) as client:
            yield client


@pytest.fixture
async def async_websocket_session(
    async_test_client_logged_in: AsyncClient,
    async_test_client_for_websocket: AsyncClient,
) -> AsyncIterator[AsyncWebSocketSession]:
    logger.debug("Create fixture async_websocket_session")
    cookies = {
        "Authorization": async_test_client_logged_in.cookies.get("Authorization")
    }
    try:
        async with aconnect_ws(
            "http://testserver/ws/main",
            async_test_client_for_websocket,
            cookies=cookies,
        ) as websocket_test_session:
            yield websocket_test_session
            logger.info("---------")
    except RuntimeError as e:
        if not "Attempted to exit cancel scope in a different task" in str(e):
            raise e
        else:
            logger.error("Ignore error. Caused by httpx_ws")
