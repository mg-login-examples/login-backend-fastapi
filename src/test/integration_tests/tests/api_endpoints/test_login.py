import logging

import requests

from data.schemas.users.userDeep import User as UserDeep
from data.schemas.users.userCreate import UserCreate
from test.utils.api import authentication as authentication_api

logger = logging.getLogger(__name__)

# Test that a user can login with email and password
def test_valid_login(test_client: requests.Session, user_login: UserCreate, created_user_by_admin: UserDeep):
    assert test_client.cookies.get("Authorization") is None
    login_response = authentication_api.login(test_client, user_login)
    assert login_response.user.id == created_user_by_admin.id
    assert login_response.access_token is not None
    assert test_client.cookies.get("Authorization") is not None

# TODO
# def test_invalid_email():
#     pass

# def test_invalid_password():
#     pass
