import logging
from typing import List

import requests
import pytest

from data.schemas.users.userDeep import User as UserDeep
from test.integration_tests.fixtures.client import test_client
from test.integration_tests.fixtures.users_admin import created_user_by_admin, created_n_users_by_admin, generate_random_user_to_create
from test.integration_tests.fixtures.dbutils import setup_db
from test.integration_tests.utils import asserts


logger = logging.getLogger(__name__)

# Test that a user can be fetched by id
def test_get_user(test_client: requests.Session, created_user_by_admin: UserDeep):
    response = test_client.get(f"/api/admin/resource/users/{created_user_by_admin.id}/")
    assert response.status_code == 200
    user = UserDeep(**response.json())
    assert user.id == created_user_by_admin.id
    assert user == created_user_by_admin

# Test that a user can be created
def test_create_user(test_client: requests.Session):
    user = generate_random_user_to_create()
    response = test_client.post("/api/admin/resource/users/", json=user.dict())
    assert response.status_code == 200
    created_user = UserDeep(**response.json())
    assert created_user.email == user.email
    assert created_user.id is not None

# Test that multiple users can be fetched
@pytest.mark.parametrize("created_n_users_by_admin", [5], indirect=True)
def test_get_users(test_client: requests.Session, created_n_users_by_admin: List[UserDeep]):
    response = test_client.get(f"/api/admin/resource/users/?skip=0&limit=4")
    assert response.status_code == 200
    assert isinstance(response.json(), List)
    users = [UserDeep(**user_json) for user_json in response.json()]
    assert len(users) == 4
    for user in users:
        assert user.id is not None

# Test that a user can be updated
def test_put_user(test_client: requests.Session, created_user_by_admin: UserDeep):
    assert created_user_by_admin.is_active
    created_user_by_admin.is_active = False
    response = test_client.put(f"/api/admin/resource/users/{created_user_by_admin.id}/", json=created_user_by_admin.dict())
    assert response.status_code == 204
    response = test_client.get(f"/api/admin/resource/users/{created_user_by_admin.id}/")
    assert response.status_code == 200
    user = UserDeep(**response.json())
    assert not user.is_active

# Test that a user can be deleted by id
def test_delete_user(test_client: requests.Session, created_user_by_admin: UserDeep):
    response = test_client.delete(f"/api/admin/resource/users/{created_user_by_admin.id}/")
    assert response.status_code == 204
    response = test_client.get(f"/api/admin/resource/users/{created_user_by_admin.id}/")
    assert response.status_code == 404
    asserts.assert_response_error_item_not_found(response)
