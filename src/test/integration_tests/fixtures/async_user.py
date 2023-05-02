import logging

import pytest
from httpx import AsyncClient

from data.schemas.authentication.login_response import LoginResponse
from data.schemas.users.userCreate import UserCreate
from data.schemas.users.user import User
from data.schemas.users.userDeep import User as UserDeep

logger = logging.getLogger(__name__)

@pytest.fixture
async def async_created_user_by_admin(async_test_client_admin_logged_in: AsyncClient, user_login: UserCreate) -> UserDeep:
    logger.debug("Create fixture async_created_user_by_admin")
    response = await async_test_client_admin_logged_in.post(
        "/api/admin/resource/users/",
        json=user_login.dict()
    )
    assert response.status_code == 200
    created_unverified_user_by_admin = UserDeep(**response.json())
    created_unverified_user_by_admin.is_verified = True
    response = await async_test_client_admin_logged_in.put(
        f"/api/admin/resource/users/{created_unverified_user_by_admin.id}/",
        json=created_unverified_user_by_admin.dict()
    )
    assert response.status_code == 204
    return created_unverified_user_by_admin

@pytest.fixture
async def async_login_response(async_test_client: AsyncClient, user_login: UserCreate, async_created_user_by_admin: User) -> LoginResponse:
    logger.debug("Create fixture async_login_response")
    response = await async_test_client.post(
        f"/api/login/",
        data={"username": user_login.email, "password": user_login.password}
    )
    assert response.status_code == 200
    return LoginResponse(**response.json())

@pytest.fixture
async def async_logged_in_user(async_login_response: LoginResponse) -> User:
    logger.debug("Create fixture async_logged_in_user")
    return async_login_response.user
