from distutils.log import Log
import pytest
import requests

from data.schemas.login.login_response import LoginResponse
from data.schemas.users.user import User
from data.schemas.users.userCreate import UserCreate
from test.utils.api import authentication as authentication_api

@pytest.fixture
def login_response(test_client: requests.Session, user_login: UserCreate, created_user_by_admin: User) -> LoginResponse:
    return authentication_api.login(test_client, user_login)

@pytest.fixture
def test_client_logged_in(test_client: requests.Session, login_response: LoginResponse) -> requests.Session:
    return test_client

@pytest.fixture
def logged_in_unverified_user(test_client: requests.Session, user_login: UserCreate, created_unverified_user_by_admin: User) -> User:
    login_response = authentication_api.login(test_client, user_login)
    return login_response.user

@pytest.fixture
def logged_in_user(login_response: LoginResponse) -> User:
    return login_response.user
