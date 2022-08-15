import logging
from unittest.mock import MagicMock, patch, ANY

import requests
from sqlalchemy.orm import Session

from data.schemas.users.user import User
from crud_endpoints_generator import crud_base
from data.database.models.user_email_verification import UserEmailVerification as UserEmailVerificationModel
from test.integration_tests.utils.fake_user import generate_random_user_to_create
from test.utils.api import users as users_api

logger = logging.getLogger(__name__)

# Test that a user can be fetched by id
def test_get_user(test_client_logged_in: requests.Session, logged_in_user: User):
    user = users_api.get_user(test_client_logged_in, logged_in_user.id)
    assert user.id == logged_in_user.id

# Test that a user can be created
@patch("background_tasks.emails.send_email")
def test_create_user(mock_send_email: MagicMock, test_client: requests.Session, db_session: Session):
    user = generate_random_user_to_create()
    created_user = users_api.create_user(test_client, user)
    assert created_user.email == user.email
    assert created_user.id is not None
    assert created_user.is_active == True
    assert created_user.is_verified == False
    # assert (mocked) send email function is called with user email
    mock_send_email.assert_called_once_with(created_user.email, ANY, ANY)
    # assert email verification record exists in db
    db_email_verifications = crud_base.get_resource_items_by_attribute(db_session, UserEmailVerificationModel, UserEmailVerificationModel.user_id, created_user.id)
    assert len(db_email_verifications) == 1
    # assert email message contains verification code
    email_message = mock_send_email.mock_calls[0].args[2]
    verification_code = db_email_verifications[0].verification_code
    assert str(verification_code) in email_message

