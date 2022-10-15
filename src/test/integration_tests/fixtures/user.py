import logging
from typing import List

import pytest
import requests

from data.schemas.authentication.login_response import LoginResponse
from data.schemas.users.userCreate import UserCreate
from data.schemas.users.user import User
from data.schemas.users.userDeep import User as UserDeep
from test.integration_tests.utils.fake_user import generate_random_user_to_create
from test.utils.admin_api import users as users_admin_api
from test.utils.user_api import authentication as authentication_api
from test.integration_tests.utils.async_testclient_for_websockets import AsyncioTestClient

logger = logging.getLogger(__name__)

@pytest.fixture
def user_login() -> UserCreate:
    return generate_random_user_to_create()

@pytest.fixture
def created_unverified_user_by_admin(test_client_admin_logged_in: requests.Session, user_login: UserCreate) -> UserDeep:
    return users_admin_api.create_user(test_client_admin_logged_in, user_login)

@pytest.fixture
def created_user_by_admin(test_client_admin_logged_in: requests.Session, created_unverified_user_by_admin: UserDeep) -> UserDeep:
    created_unverified_user_by_admin.is_verified = True
    users_admin_api.put_user(test_client_admin_logged_in, created_unverified_user_by_admin)
    return created_unverified_user_by_admin

@pytest.fixture
def login_response(test_client: requests.Session, user_login: UserCreate, created_user_by_admin: User) -> LoginResponse:
    return authentication_api.login(test_client, user_login)

@pytest.fixture
def logged_in_unverified_user(test_client: requests.Session, user_login: UserCreate, created_unverified_user_by_admin: User) -> User:
    login_response = authentication_api.login(test_client, user_login)
    return login_response.user

@pytest.fixture
def logged_in_user(login_response: LoginResponse) -> User:
    return login_response.user

@pytest.fixture
def created_n_users_by_admin(test_client_admin_logged_in: requests.Session, n_users: int = 5) -> List[UserDeep]:
    users = []
    for _ in range(n_users):
        user = generate_random_user_to_create()
        users.append(
            users_admin_api.create_user(test_client_admin_logged_in, user)
        )
    return users

@pytest.fixture
def user_2_login() -> UserCreate:
    return generate_random_user_to_create()

@pytest.fixture
def created_user_2_by_admin(test_client_admin_logged_in: requests.Session, user_2_login: UserCreate) -> UserDeep:
    user_2 = users_admin_api.create_user(test_client_admin_logged_in, user_2_login)
    user_2.is_verified = True
    users_admin_api.put_user(test_client_admin_logged_in, user_2)
    return user_2
