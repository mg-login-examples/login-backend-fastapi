import requests  # type: ignore

from data.schemas.admin_login.admin_login_response import AdminLoginResponse
from data.schemas.admin_users.admin_user import AdminUser
from data.schemas.admin_users.admin_user_create import AdminUserCreate


def login(
    test_client: requests.Session, admin_user: AdminUserCreate
) -> AdminLoginResponse:
    response = test_client.post(
        f"/api/admin/login/",
        data={"username": admin_user.email, "password": admin_user.password},
    )
    assert response.status_code == 200
    return AdminLoginResponse(**response.json())


def authenticate(test_client: requests.Session) -> AdminUser:
    response = test_client.post("/api/admin/authenticate/")
    assert response.status_code == 200
    return AdminUser(**response.json())
