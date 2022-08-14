import logging

import requests

from data.schemas.users.user import User
from test.integration_tests.utils.fake_user import generate_random_user_to_create
from test.utils.api import users as users_api

logger = logging.getLogger(__name__)

# Test that a user can be fetched by id
def test_get_user(test_client_logged_in: requests.Session, logged_in_user: User):
    user = users_api.get_user(test_client_logged_in, logged_in_user.id)
    assert user.id == logged_in_user.id

# Test that a user can be created
def test_create_user(test_client: requests.Session):
    user = generate_random_user_to_create()
    created_user = users_api.create_user(test_client, user)
    assert created_user.email == user.email
    assert created_user.id is not None
    assert created_user.is_active == True
    assert created_user.is_verified == False
