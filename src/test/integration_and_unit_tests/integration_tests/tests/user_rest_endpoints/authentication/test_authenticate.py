import logging
import random
import string

import requests

from data.schemas.authentication.login_response import LoginResponse
from data.schemas.users.user import User
from data.schemas.users.userDeep import User as UserDeep
from test.integration_and_unit_tests.utils.user_api import authentication as authentication_api

logger = logging.getLogger(__name__)

authenticate_url = "api/authenticate/"


def test_authentication_standard_flow(
        login_response: LoginResponse, test_client_logged_in: requests.Session):
    user = authentication_api.authenticate(test_client_logged_in)
    assert user.id == login_response.user.id


def test_authentication_no_access_token(
        test_client_logged_in: requests.Session):
    test_client_logged_in.cookies.pop("Authorization")
    response = test_client_logged_in.post(authenticate_url)
    assert response.status_code == 403
    assert response.cookies.get("Authorization") is None


def test_authentication_valid_cookie(
        created_user_by_admin: UserDeep, login_response: LoginResponse, test_client_logged_in: requests.Session):
    authorization_cookie = test_client_logged_in.cookies.get("Authorization")
    assert authorization_cookie == f'"Bearer {login_response.access_token}"'
    response = test_client_logged_in.post(authenticate_url)
    assert response.status_code == 200
    user = User(**response.json())
    assert user.id == created_user_by_admin.id


def test_authentication_valid_header(
        created_user_by_admin: UserDeep, login_response: LoginResponse, test_client_logged_in: requests.Session):
    test_client_logged_in.cookies.pop("Authorization")
    response = test_client_logged_in.post(
        authenticate_url,
        headers={"Authorization": f"Bearer {login_response.access_token}"}
    )
    assert response.status_code == 200
    user = User(**response.json())
    assert user.id == created_user_by_admin.id


def test_authentication_invalid_authorization_cookie_non_existing_value(
        test_client_logged_in: requests.Session):
    test_client_logged_in.cookies.pop("Authorization")
    test_client_logged_in.cookies.set(
        "Authorization", '"Bearer invalid-cookie"')
    response = test_client_logged_in.post(authenticate_url)
    assert response.status_code == 403
    assert response.cookies.get("Authorization") is None


def test_authentication_invalid_authorization_cookie_no_bearer(
        login_response: LoginResponse, test_client_logged_in: requests.Session):
    test_client_logged_in.cookies.pop("Authorization")
    test_client_logged_in.cookies.set(
        "Authorization", f'"{login_response.access_token}"')
    response = test_client_logged_in.post(authenticate_url)
    assert response.status_code == 403
    assert response.cookies.get("Authorization") is None


def test_authentication_invalid_authorization_header_non_existing_value(
        test_client_logged_in: requests.Session):
    test_client_logged_in.cookies.pop("Authorization")
    response = test_client_logged_in.post(
        authenticate_url,
        headers={"Authorization": f"Bearer invalid-cookie"}
    )
    assert response.status_code == 403
    assert response.cookies.get("Authorization") is None


def test_authentication_invalid_authorization_header_no_bearer(
        login_response: LoginResponse, test_client_logged_in: requests.Session):
    test_client_logged_in.cookies.pop("Authorization")
    response = test_client_logged_in.post(
        authenticate_url,
        headers={"Authorization": f"{login_response.access_token}"}
    )
    assert response.status_code == 403
    assert response.cookies.get("Authorization") is None
