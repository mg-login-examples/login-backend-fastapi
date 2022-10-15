import logging
from asyncio import AbstractEventLoop

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from test.integration_tests.utils.async_testclient_for_websockets import AsyncioTestClient, AsyncioWebSocketTestSession

logger = logging.getLogger(__name__)

@pytest.fixture
async def async_test_client_for_websocket(event_loop: AbstractEventLoop, app: FastAPI) -> AsyncioTestClient:
    async with AsyncioTestClient(app, event_loop=event_loop) as client:
        yield client

@pytest.fixture
async def async_websocket_session(async_test_client_logged_in: AsyncClient, async_test_client_for_websocket: AsyncioTestClient) -> AsyncioWebSocketTestSession:
    cookies={"Authorization": async_test_client_logged_in.cookies.get("Authorization")}
    async with async_test_client_for_websocket.websocket_connect("/ws/main", cookies=cookies) as websocket:
        yield websocket
