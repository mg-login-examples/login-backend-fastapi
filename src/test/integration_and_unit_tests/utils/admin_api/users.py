import logging

import requests

from data.schemas.users.userDeep import User as UserDeep
from data.schemas.users.userCreate import UserCreate
from test.integration_and_unit_tests.integration_tests.utils import asserts

logger = logging.getLogger(__name__)

def get_user(test_client: requests.Session, user_id: int) -> UserDeep:
    response = test_client.get(f"/api/admin/resource/users/{user_id}/")
    assert response.status_code == 200
    return UserDeep(**response.json())

def create_user(test_client: requests.Session, user_to_create: UserCreate) -> UserDeep:
    response = test_client.post("/api/admin/resource/users/", json=user_to_create.model_dump())
    assert response.status_code == 200
    return UserDeep(**response.json())

def put_user(test_client: requests.Session, user_to_edit: UserDeep):
    response = test_client.put(f"/api/admin/resource/users/{user_to_edit.id}/", json=user_to_edit.model_dump())
    assert response.status_code == 204

def delete_user(test_client: requests.Session, user_id: int):
    response = test_client.delete(f"/api/admin/resource/users/{user_id}/")
    assert response.status_code == 204

def get_users(test_client: requests.Session, skip=0, limit=10) -> list[UserDeep]:
    response = test_client.get(f"/api/admin/resource/users/?skip={skip}&limit={limit}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    users = [UserDeep(**user_json) for user_json in response.json()]
    return users

def get_user_expect_not_found(test_client: requests.Session, user_id: int):
    response = test_client.get(f"/api/admin/resource/users/{user_id}/")
    assert response.status_code == 404
    asserts.assert_response_error_item_not_found(response)
