import logging

import requests

from data.schemas.users.user import User
from test.integration_tests.utils.fake_user import generate_random_user_to_create
from test.utils.api import users as users_api

logger = logging.getLogger(__name__)

# Test that a user can be fetched by id
def test_get_user(test_client: requests.Session, created_user: User):
    user = users_api.get_user(test_client, created_user.id)
    assert user.id == created_user.id

# Test that a user can be created
def test_create_user(test_client: requests.Session):
    user_to_create = generate_random_user_to_create()
    created_user = users_api.create_user(test_client, user_to_create)
    assert created_user.email == user_to_create.email
    assert created_user.id is not None
