import requests

from data.schemas.login.login_response import LoginResponse
from data.schemas.users.userCreate import UserCreate

def login(test_client: requests.Session, user: UserCreate) -> LoginResponse:
    response = test_client.post(
        f"/api/login/",
        data={"username": user.email, "password": user.password}
    )
    assert response.status_code == 200
    return LoginResponse(**response.json())
