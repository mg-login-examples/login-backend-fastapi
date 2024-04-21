import requests  # type: ignore

from data.schemas.authentication.login_response import LoginResponse
from data.schemas.user_sessions.userSession import UserSession
from data.schemas.users.user import User
from data.schemas.users.userCreate import UserCreate


def get_user(test_client: requests.Session, user_id: int) -> User:
    response = test_client.get(f"/api/users/{user_id}/")
    assert response.status_code == 200
    return User(**response.json())


def create_user(test_client: requests.Session, user_to_create: UserCreate) -> User:
    response = test_client.post("/api/users/", json=user_to_create.model_dump())
    assert response.status_code == 200
    loginResponse = LoginResponse(**response.json())
    return loginResponse.user


def get_user_sessions(
    test_client: requests.Session, user_id: int, skip=0, limit=10
) -> list[UserSession]:
    response = test_client.get(
        f"/api/users/{user_id}/sessions/?skip={skip}&limit={limit}"
    )
    assert response.status_code == 200
    user_sessions = [
        UserSession(**user_session_json) for user_session_json in response.json()
    ]
    return user_sessions
