import pytest
import requests

from data.schemas.login.login_response import LoginResponse
from data.schemas.users.user import User
from data.schemas.users.userCreate import UserCreate
from test.utils.api import authentication as authentication_api

@pytest.fixture
def login_response(test_client: requests.Session, user_data: UserCreate, created_user: User) -> LoginResponse:
    return authentication_api.login(test_client, user_data)

@pytest.fixture
def test_client_authenticated(test_client: requests.Session, login_response: LoginResponse) -> requests.Session:
    return test_client
