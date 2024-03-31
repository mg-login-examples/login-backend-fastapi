from asyncio import AbstractEventLoop
import pytest
from typing import AsyncIterator

from fastapi import FastAPI
from httpx import AsyncClient
from asgi_lifespan import LifespanManager

from utils.pubsub.pubsub import PubSub
from data.schemas.admin_login.admin_login_response import AdminLoginResponse
from data.schemas.authentication.login_response import LoginResponse

import logging
logger = logging.getLogger(__name__)


@pytest.fixture
async def async_test_client(app: FastAPI, app_pubsub: PubSub) -> AsyncIterator[AsyncClient]:
    logger.debug("Create fixture async_test_client")
    # async with LifespanManager(app):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
        # FastAPI shutdown not called by httpx AsyncClient so need to manually disconnect PubSub
        # Otherwise get Error 'Task was destroyed but it is pending!' & 'Event
        # loop is closed' in PubSub _listener task
        logger.debug("Destroying fixture async_test_client")
        await app_pubsub.disconnect()
        logger.debug("Destroyed fixture async_test_client")


@pytest.fixture
async def async_test_client_admin_logged_in(
        async_test_client: AsyncClient, async_admin_login_response: AdminLoginResponse) -> AsyncClient:
    logger.debug("Create fixture async_test_client_admin_logged_in")
    return async_test_client


@pytest.fixture
async def async_test_client_logged_in(
        async_test_client: AsyncClient, async_login_response: LoginResponse) -> AsyncClient:
    logger.debug("Create fixture async_test_client_logged_in")
    return async_test_client
