import logging

import requests

from data.schemas.users.user import User
from data.schemas.users.userCreate import UserCreate
from test.utils.api import authentication as authentication_api

logger = logging.getLogger(__name__)

# Test that a user can login with email and password
def test_valid_login(test_client: requests.Session, user_data: UserCreate, created_user: User):
    login_response = authentication_api.login(test_client, user_data)
    assert int(login_response.id) == created_user.id
    assert login_response.access_token is not None

# def test_invalid_email():
#     pass

# def test_invalid_password():
#     pass
