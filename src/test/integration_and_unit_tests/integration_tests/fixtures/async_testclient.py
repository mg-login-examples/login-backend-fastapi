import logging
from asyncio import AbstractEventLoop
from typing import AsyncIterator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import AsyncClient

from data.schemas.admin_login.admin_login_response import AdminLoginResponse
from data.schemas.authentication.login_response import LoginResponse
from utils.pubsub.pubsub import PubSub

logger = logging.getLogger(__name__)


@pytest.fixture
async def async_test_client(
    app: FastAPI, app_pubsub: PubSub
) -> AsyncIterator[AsyncClient]:
    logger.debug("Create fixture async_test_client")
    # async with LifespanManager(app):
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def async_test_client_admin_logged_in(
    async_test_client: AsyncClient, async_admin_login_response: AdminLoginResponse
) -> AsyncClient:
    logger.debug("Create fixture async_test_client_admin_logged_in")
    return async_test_client


@pytest.fixture
async def async_test_client_logged_in(
    async_test_client: AsyncClient, async_login_response: LoginResponse
) -> AsyncClient:
    logger.debug("Create fixture async_test_client_logged_in")
    return async_test_client
