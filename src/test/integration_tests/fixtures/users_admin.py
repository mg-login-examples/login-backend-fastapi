import logging
from typing import List

import pytest
import requests

from test.integration_tests.utils.fake_user import generate_random_user_to_create
from test.utils.admin_api import users as users_admin_api
from data.schemas.users.userCreate import UserCreate
from data.schemas.users.userDeep import User as UserDeep

logger = logging.getLogger(__name__)

@pytest.fixture
def user_login() -> UserCreate:
    return generate_random_user_to_create()

@pytest.fixture
def created_user_by_admin(test_client_admin_logged_in: requests.Session, user_login: UserCreate) -> UserDeep:
    return users_admin_api.create_user(test_client_admin_logged_in, user_login)

@pytest.fixture
def created_n_users_by_admin(test_client_admin_logged_in: requests.Session, n_users: int = 5) -> List[UserDeep]:
    users = []
    for _ in range(n_users):
        user = generate_random_user_to_create()
        users.append(
            users_admin_api.create_user(test_client_admin_logged_in, user)
        )
    return users
