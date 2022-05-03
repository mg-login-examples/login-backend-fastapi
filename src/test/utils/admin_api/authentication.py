import requests

from data.schemas.login.login_response import LoginResponse
from data.schemas.admin_users.admin_user_create import AdminUserCreate
from data.schemas.admin_users.admin_user import AdminUser

def login(test_client: requests.Session, admin_user: AdminUserCreate) -> LoginResponse:
    response = test_client.post(
        f"/api/admin/login/",
        data={"username": admin_user.email, "password": admin_user.password}
    )
    assert response.status_code == 200
    return LoginResponse(**response.json())

def authenticate(test_client: requests.Session) -> LoginResponse:
    response = test_client.post("/api/admin/authenticate/")
    assert response.status_code == 200
    return AdminUser(**response.json())
