from asyncio import AbstractEventLoop

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from data.schemas.admin_login.admin_login_response import AdminLoginResponse
from data.schemas.authentication.login_response import LoginResponse

@pytest.fixture
async def async_test_client(event_loop: AbstractEventLoop, app: FastAPI) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

@pytest.fixture
async def async_test_client_admin_logged_in(async_test_client: AsyncClient, async_admin_login_response: AdminLoginResponse) -> AsyncClient:
    return async_test_client

@pytest.fixture
async def async_test_client_logged_in(async_test_client: AsyncClient, async_login_response: LoginResponse) -> AsyncClient:
    return async_test_client
