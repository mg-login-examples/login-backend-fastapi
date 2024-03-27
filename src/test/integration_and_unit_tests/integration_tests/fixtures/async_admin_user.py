import pytest
import logging

from httpx import AsyncClient

from data.schemas.admin_login.admin_login_response import AdminLoginResponse
from data.schemas.admin_users.admin_user import AdminUser
from data.schemas.admin_users.admin_user_create import AdminUserCreate

logger = logging.getLogger(__name__)


@pytest.fixture
async def async_admin_login_response(
        async_test_client: AsyncClient, admin_user_login: AdminUserCreate) -> AdminLoginResponse:
    logger.debug("Create fixture async_admin_login_response")
    response = await async_test_client.post(
        f"/api/admin/login/",
        data={"username": admin_user_login.email,
              "password": admin_user_login.password}
    )
    assert response.status_code == 200
    return AdminLoginResponse(**response.json())


@pytest.fixture
async def async_logged_in_admin_user(
        async_test_client_admin_logged_in: AsyncClient) -> AdminUser:
    logger.debug("Create fixture async_logged_in_admin_user")
    response = await async_test_client_admin_logged_in.post("/api/admin/authenticate/")
    assert response.status_code == 200
    return AdminUser(**response.json())
