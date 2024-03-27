import requests

from data.schemas.authentication.login_response import LoginResponse
from data.schemas.authentication.user_password_change import UserPasswordChange
from data.schemas.users.userCreate import UserCreate
from data.schemas.users.user import User
from test.integration_and_unit_tests.integration_tests.utils import asserts


def login(test_client: requests.Session, user: UserCreate) -> LoginResponse:
    response = test_client.post(
        f"/api/login/",
        data={"username": user.email, "password": user.password}
    )
    assert response.status_code == 200
    return LoginResponse(**response.json())


def authenticate(test_client: requests.Session) -> LoginResponse:
    response = test_client.post("/api/authenticate/")
    assert response.status_code == 200
    return User(**response.json())


def logout(test_client: requests.Session) -> None:
    response = test_client.post("/api/logout/")
    assert response.status_code == 204


def login_expect_unauthorized(test_client: requests.Session, user: UserCreate):
    response = test_client.post(
        f"/api/login/",
        data={"username": user.email, "password": user.password}
    )
    assert response.status_code == 401
    asserts.assert_response_error_invalid_login(response)


def password_change(test_client: requests.Session,
                    user_password_change: UserPasswordChange):
    response = test_client.post(
        "/api/password-change/", json=user_password_change.model_dump())
    assert response.status_code == 200
    return LoginResponse(**response.json())
