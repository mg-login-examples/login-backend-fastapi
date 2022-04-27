import requests

from data.schemas.users.user import User
from data.schemas.users.userCreate import UserCreate


def get_user(test_client: requests.Session, user_id: int) -> User:
    response = test_client.get(f"/api/users/{user_id}/")
    assert response.status_code == 200
    return User(**response.json())

def create_user(test_client: requests.Session, user_to_create: UserCreate) -> User:
    response = test_client.post("/api/users/", json=user_to_create.dict())
    assert response.status_code == 200
    return User(**response.json())
