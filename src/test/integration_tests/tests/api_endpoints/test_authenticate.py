import logging

import requests

from data.schemas.login.login_response import LoginResponse
from data.schemas.users.user import User
from data.schemas.users.user import User
# from test.utils.api import authentication as authentication_api

logger = logging.getLogger(__name__)

authenticate_url = "api/authenticate/"

def test_authentication_no_access_token(test_client_authenticated: requests.Session):
    test_client_authenticated.cookies.pop("Authorization")
    response = test_client_authenticated.post(authenticate_url)
    assert response.status_code == 403

def test_authentication_valid_cookie(created_user: User, login_response: LoginResponse, test_client_authenticated: requests.Session):
    authorization_cookie = test_client_authenticated.cookies.get("Authorization")
    assert authorization_cookie == f'"Bearer {login_response.access_token}"'
    response = test_client_authenticated.post(authenticate_url)
    assert response.status_code == 200
    user = User(**response.json())
    assert user.id == created_user.id

def test_authentication_valid_header(created_user: User, login_response: LoginResponse, test_client_authenticated: requests.Session):
    test_client_authenticated.cookies.pop("Authorization")
    response = test_client_authenticated.post(
        authenticate_url,
        headers={"Authorization": f"Bearer {login_response.access_token}"}
    )
    assert response.status_code == 200
    user = User(**response.json())
    assert user.id == created_user.id

def test_authentication_invalid_cookie_wrong_access_token(test_client_authenticated: requests.Session):
    test_client_authenticated.cookies.pop("Authorization")
    test_client_authenticated.cookies.set("Authorization", '"Bearer invalid-cookie"')
    response = test_client_authenticated.post(authenticate_url)
    assert response.status_code == 403

def test_authentication_invalid_cookie_no_bearer(login_response: LoginResponse, test_client_authenticated: requests.Session):
    test_client_authenticated.cookies.pop("Authorization")
    test_client_authenticated.cookies.set("Authorization", f'"{login_response.access_token}"')
    response = test_client_authenticated.post(authenticate_url)
    assert response.status_code == 403

def test_authentication_invalid_header_wrong_access_token(test_client_authenticated: requests.Session):
    test_client_authenticated.cookies.pop("Authorization")
    response = test_client_authenticated.post(
        authenticate_url,
        headers={"Authorization": f"Bearer invalid-cookie"}
    )
    assert response.status_code == 403

def test_authentication_invalid_cookie_no_bearer(login_response: LoginResponse, test_client_authenticated: requests.Session):
    test_client_authenticated.cookies.pop("Authorization")
    response = test_client_authenticated.post(
        authenticate_url,
        headers={"Authorization": f"{login_response.access_token}"}
    )
    assert response.status_code == 403
