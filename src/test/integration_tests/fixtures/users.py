import logging
from typing import List
import random
import string

import pytest
import requests

from test.integration_tests.fixtures.client import test_client
from data.schemas.users.userCreate import UserCreate
from data.schemas.users.user import User

logger = logging.getLogger(__name__)

def generate_random_user_to_create() -> UserCreate:
    user_email = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    user_password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    user = UserCreate(email=user_email, password=user_password)
    return user

@pytest.fixture
def created_user(test_client: requests.Session) -> User:
    user = generate_random_user_to_create()
    response = test_client.post("/api/users/", json=user.dict())
    assert response.status_code == 200
    return User(**response.json())

@pytest.fixture
def created_n_users(test_client: requests.Session, n_users: int = 5) -> List[User]:
    users = []
    for _ in range(n_users):
        user = generate_random_user_to_create()
        response = test_client.post("/api/users/", json=user.dict())
        assert response.status_code == 200
        users.append(
            User(**response.json())
        )
    return users
