import pytest
import requests

from data.schemas.login.login_response import LoginResponse
from data.schemas.admin_users.admin_user import AdminUser
from data.schemas.admin_users.admin_user_create import AdminUserCreate
from test.utils.admin_api import authentication as admin_authentication_api

@pytest.fixture
def admin_user_login() -> AdminUserCreate:
    return AdminUserCreate(email="admin@admin.admin", password="admin")

@pytest.fixture
def admin_login_response(test_client: requests.Session, admin_user_login: AdminUserCreate) -> LoginResponse:
    return admin_authentication_api.login(test_client, admin_user_login)

@pytest.fixture
def test_client_admin_logged_in(test_client: requests.Session, admin_login_response: LoginResponse) -> requests.Session:
    return test_client

@pytest.fixture
def logged_in_admin_user(test_client_admin_logged_in: requests.Session) -> AdminUser:
    return admin_authentication_api.authenticate(test_client_admin_logged_in)
