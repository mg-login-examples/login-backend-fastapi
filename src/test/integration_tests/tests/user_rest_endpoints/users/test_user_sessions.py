import logging
from unittest.mock import MagicMock, patch, ANY

import requests

from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager
from data.schemas.users.user import User
from test.utils.user_api import users as users_api
from test.integration_tests.utils import asserts

logger = logging.getLogger(__name__)

# Test that a logged in user's sessions can be fetched
def test_get_user_sessions(test_client_logged_in: requests.Session, logged_in_user: User):
    user_sessions = users_api.get_user_sessions(test_client_logged_in, logged_in_user.id)
    assert len(user_sessions) == 1
    assert user_sessions[0].user_id == logged_in_user.id

# Test that a logged in user's sessions can be fetched
def test_get_user_sessions_fails_when_getting_different_user_than_logged_in(
    test_client_logged_in: requests.Session,
    logged_in_user: User,
    created_user_2_by_admin: User
):
    assert logged_in_user.id != created_user_2_by_admin.id
    response = test_client_logged_in.get(f"/api/users/{created_user_2_by_admin.id}/sessions/")
    assert response.status_code == 403
    asserts.assert_response_error_resource_not_accessible(response)
