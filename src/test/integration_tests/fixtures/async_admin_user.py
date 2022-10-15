import pytest
from httpx import AsyncClient

from data.schemas.admin_login.admin_login_response import AdminLoginResponse
from data.schemas.admin_users.admin_user import AdminUser
from data.schemas.admin_users.admin_user_create import AdminUserCreate

@pytest.fixture
async def async_admin_login_response(async_test_client: AsyncClient, admin_user_login: AdminUserCreate) -> AdminLoginResponse:
    response = await async_test_client.post(
        f"/api/admin/login/",
        data={"username": admin_user_login.email, "password": admin_user_login.password}
    )
    assert response.status_code == 200
    return AdminLoginResponse(**response.json())

@pytest.fixture
async def async_logged_in_admin_user(async_test_client_admin_logged_in: AsyncClient) -> AdminUser:
    response = await async_test_client_admin_logged_in.post("/api/admin/authenticate/")
    assert response.status_code == 200
    return AdminUser(**response.json())
