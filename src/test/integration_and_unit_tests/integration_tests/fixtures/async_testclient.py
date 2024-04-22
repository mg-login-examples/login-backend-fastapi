import logging
import typing
from typing import AsyncIterator, cast

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from data.schemas.admin_login.admin_login_response import AdminLoginResponse
from data.schemas.authentication.login_response import LoginResponse
from utils.pubsub.pubsub import PubSub

logger = logging.getLogger(__name__)

# type magic
_Message = typing.Dict[str, typing.Any]
_Receive = typing.Callable[[], typing.Awaitable[_Message]]
_Send = typing.Callable[
    [typing.Dict[str, typing.Any]], typing.Coroutine[None, None, None]
]
_ASGIApp = typing.Callable[
    [typing.Dict[str, typing.Any], _Receive, _Send], typing.Coroutine[None, None, None]
]


@pytest.fixture
async def async_test_client(
    app: FastAPI, app_pubsub: PubSub
) -> AsyncIterator[AsyncClient]:
    logger.debug("Create fixture async_test_client")
    async with LifespanManager(app):
        app_asgi = cast(_ASGIApp, app)
        async with AsyncClient(
            transport=ASGITransport(app_asgi), base_url="http://test"
        ) as client:
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
