import logging
from typing import List

import requests
import pytest

from data.schemas.users.userDeep import User as UserDeep
from test.integration_tests.utils.fake_user import generate_random_user_to_create
from test.utils.admin_api import users as users_admin_api

logger = logging.getLogger(__name__)

# Test that a user can be fetched by id
def test_get_user(test_client: requests.Session, created_user_by_admin: UserDeep):
    user = users_admin_api.get_user(test_client, created_user_by_admin.id)
    assert user.id == created_user_by_admin.id
    assert user == created_user_by_admin

# Test that a user can be created
def test_create_user(test_client: requests.Session):
    user = generate_random_user_to_create()
    created_user = users_admin_api.create_user(test_client, user)
    assert created_user.email == user.email
    assert created_user.id is not None

# Test that multiple users can be fetched
@pytest.mark.parametrize("created_n_users_by_admin", [5], indirect=True)
def test_get_users(test_client: requests.Session, created_n_users_by_admin: List[UserDeep]):
    users = users_admin_api.get_users(test_client, limit=4)
    assert len(users) == 4
    for user in users:
        assert user.id is not None

# Test that a user can be updated
def test_put_user(test_client: requests.Session, created_user_by_admin: UserDeep):
    assert created_user_by_admin.is_active
    created_user_by_admin.is_active = False
    users_admin_api.put_user(test_client, created_user_by_admin)
    user = users_admin_api.get_user(test_client, created_user_by_admin.id)
    assert not user.is_active

# Test that a user can be deleted by id
def test_delete_user(test_client: requests.Session, created_user_by_admin: UserDeep):
    users_admin_api.delete_user(test_client, created_user_by_admin.id)
    users_admin_api.get_user_expect_not_found(test_client, created_user_by_admin.id)
