import logging
import random
import string

import requests

from data.schemas.authentication.login_response import LoginResponse
from data.schemas.authentication.user_password_change import UserPasswordChange
from data.schemas.users.userCreate import UserCreate
from data.schemas.users.userDeep import User as UserDeep
from test.integration_and_unit_tests.utils.user_api import authentication as authentication_api

logger = logging.getLogger(__name__)


def test_user_password_change(user_login: UserCreate, login_response: LoginResponse,
                              created_user_by_admin: UserDeep, test_client_logged_in: requests.Session):
    old_token = test_client_logged_in.cookies.get("Authorization")

    new_user_password = ''.join(random.choices(
        string.ascii_uppercase + string.digits, k=8))
    user_password_change = UserPasswordChange(
        username=user_login.email,
        password=user_login.password,
        password_new=new_user_password
    )
    login_response_new = authentication_api.password_change(
        test_client_logged_in, user_password_change)
    assert login_response_new.user.id == created_user_by_admin.id
    assert login_response_new.access_token is not None
    assert login_response_new.access_token != login_response.access_token
    assert test_client_logged_in.cookies.get("Authorization") is not None
    new_token = test_client_logged_in.cookies.get("Authorization")
    assert new_token != old_token
    user_login.password = new_user_password
    authentication_api.login(test_client_logged_in, user_login)
