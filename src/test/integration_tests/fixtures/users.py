import logging
from typing import List

import pytest
import requests

from data.schemas.users.user import User
from data.schemas.users.userCreate import UserCreate
from test.integration_tests.utils.fake_user import generate_random_user_to_create
from test.utils.api import users as users_api

logger = logging.getLogger(__name__)

@pytest.fixture
def user_data() -> str:
    return generate_random_user_to_create()

@pytest.fixture
def created_user(test_client: requests.Session, user_data: UserCreate) -> User:
    return users_api.create_user(test_client, user_data)

@pytest.fixture
def created_n_users(test_client: requests.Session, n_users: int = 5) -> List[User]:
    users = []
    for _ in range(n_users):
        user_data = generate_random_user_to_create()
        users.append(
            users_api.create_user(test_client, user_data)
        )
    return users
