import logging

import requests

from data.schemas.users.user import User
from test.integration_tests.fixtures.app import test_settings, test_app_db_manager, setup_db, test_client
from test.integration_tests.fixtures.users import created_user, generate_random_user_to_create

logger = logging.getLogger(__name__)

# Test that a user can be fetched by id
def test_get_user(test_client: requests.Session, created_user: User):
    response = test_client.get(f"/api/users/{created_user.id}/")
    assert response.status_code == 200
    user = User(**response.json())
    assert user.id == created_user.id

# Test that a user can be created
def test_create_user(test_client: requests.Session):
    user = generate_random_user_to_create()
    response = test_client.post("/api/users/", json=user.dict())
    assert response.status_code == 200
    created_user = User(**response.json())
    assert created_user.email == user.email
    assert created_user.id is not None
