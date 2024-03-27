import logging
from unittest.mock import MagicMock, patch, ANY

import requests

from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager
from data.schemas.users.user import User
from stores.sql_db_store import crud_base
from data.database.models.user_email_verification import UserEmailVerification as UserEmailVerificationModel
from test.integration_and_unit_tests.integration_tests.utils.fake_user import generate_random_user_to_create
from test.integration_and_unit_tests.utils.user_api import users as users_api
from utils.email.email_utils import send_email
from test.integration_and_unit_tests.integration_tests.utils import asserts

logger = logging.getLogger(__name__)

# Test that a logged in user can be fetched by id


def test_get_user(test_client_logged_in: requests.Session,
                  logged_in_user: User):
    user = users_api.get_user(test_client_logged_in, logged_in_user.id)
    assert user.id == logged_in_user.id

# Test that a different user than the one logged in cannot be fetched


def test_get_user_fails_when_getting_different_user_than_logged_in(
    test_client_logged_in: requests.Session,
    logged_in_user: User,
    created_user_2_by_admin: User
):
    assert logged_in_user.id != created_user_2_by_admin.id
    response = test_client_logged_in.get(
        f"/api/users/{created_user_2_by_admin.id}/")
    assert response.status_code == 403
    asserts.assert_response_error_resource_not_accessible(response)

# Test that a user can be created


@patch("fastapi.BackgroundTasks.add_task")
def test_create_user(mock_add_task: MagicMock,
                     test_client: requests.Session, app_db_manager: SQLAlchemyDBManager):
    user = generate_random_user_to_create()
    created_user = users_api.create_user(test_client, user)
    assert created_user.email == user.email
    assert created_user.id is not None
    assert created_user.is_active == True
    assert created_user.is_verified == False
    # assert email verification record exists in db
    db_session = next(app_db_manager.db_session())
    db_email_verifications = crud_base.get_resource_items_by_attribute(
        db_session, UserEmailVerificationModel, UserEmailVerificationModel.user_id, created_user.id)
    assert len(db_email_verifications) == 1
    # assert (mocked) backgroud_tasks.add_task is called
    mock_add_task.assert_called_once_with(
        send_email, created_user.email, ANY, ANY)
    # assert sent email message contains verification code
    email_message = mock_add_task.mock_calls[0].args[3]
    verification_code = db_email_verifications[0].verification_code
    assert str(verification_code) in email_message

# Test that a logged in user's sessions can be fetched


def test_get_user_sessions(
        test_client_logged_in: requests.Session, logged_in_user: User):
    user_sessions = users_api.get_user_sessions(
        test_client_logged_in, logged_in_user.id)
    assert len(user_sessions) == 1
    assert user_sessions[0].user_id == logged_in_user.id

# Test that a logged in user's sessions can be fetched


def test_get_user_sessions_fails_when_getting_different_user_than_logged_in(
    test_client_logged_in: requests.Session,
    logged_in_user: User,
    created_user_2_by_admin: User
):
    assert logged_in_user.id != created_user_2_by_admin.id
    response = test_client_logged_in.get(
        f"/api/users/{created_user_2_by_admin.id}/sessions/")
    assert response.status_code == 403
    asserts.assert_response_error_resource_not_accessible(response)
