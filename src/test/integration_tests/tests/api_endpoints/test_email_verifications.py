import logging
from unittest.mock import MagicMock, patch, ANY

import requests
from sqlalchemy.orm import Session

from crud_endpoints_generator import crud_base
from data.database.models.user_email_verification import UserEmailVerification as UserEmailVerificationModel
from data.schemas.users.user import User
from test.utils.admin_api import users as users_admin_api
from test.utils.api import email_verifications as email_verifications_api

logger = logging.getLogger(__name__)


@patch("background_tasks.emails.send_email")
def test_resend_email_unverified_user(mock_send_email: MagicMock, logged_in_unverified_user: User, test_client: requests.Session, db_session: Session):
    # assert user is not verified
    assert logged_in_unverified_user.is_verified == False
    # assert no email verifications exist for user
    db_email_verifications = crud_base.get_resource_items_by_attribute(db_session, UserEmailVerificationModel, UserEmailVerificationModel.user_id, logged_in_unverified_user.id)
    assert len(db_email_verifications) == 0
    # call send email verification endpoint
    email_verifications_api.resend_verification_email(test_client)
    # assert (mocked) send email function is called with user email
    mock_send_email.assert_called_once_with(logged_in_unverified_user.email, ANY, ANY)
    # assert email verification record exists in db
    db_email_verifications = crud_base.get_resource_items_by_attribute(db_session, UserEmailVerificationModel, UserEmailVerificationModel.user_id, logged_in_unverified_user.id)
    assert len(db_email_verifications) == 1
    # assert email message contains verification code
    email_message = mock_send_email.mock_calls[0].args[2]
    verification_code = db_email_verifications[0].verification_code
    assert str(verification_code) in email_message

@patch("background_tasks.emails.send_email")
def test_resend_email_verified_user(mock_send_email: MagicMock, test_client_logged_in: requests.Session, logged_in_user: User, db_session: Session):
    # assert user is verified
    assert logged_in_user.is_verified == True
    # assert no email verifications record exist for user in db
    db_email_verifications = crud_base.get_resource_items_by_attribute(db_session, UserEmailVerificationModel, UserEmailVerificationModel.user_id, logged_in_user.id)
    assert len(db_email_verifications) == 0

    # call send email verification endpoint
    email_verifications_api.resend_verification_email(test_client_logged_in)

    # assert (mocked) send email function is not called
    mock_send_email.assert_not_called()
    # assert no email verifications record exist for user in db
    db_email_verifications = crud_base.get_resource_items_by_attribute(db_session, UserEmailVerificationModel, UserEmailVerificationModel.user_id, logged_in_user.id)
    assert len(db_email_verifications) == 0

@patch("background_tasks.emails.send_email")
def test_verify_email(mock_send_email: MagicMock, logged_in_unverified_user: User, test_client: requests.Session, db_session: Session):
    # call send email verification endpoint to create a verification code record in db
    email_verifications_api.resend_verification_email(test_client)
    # assert user is unverified
    user = users_admin_api.get_user(test_client, logged_in_unverified_user.id)
    assert user.is_verified == False
    # retrieve verification code from db
    db_email_verification = crud_base.get_resource_item_by_attribute(db_session, UserEmailVerificationModel, UserEmailVerificationModel.user_id, logged_in_unverified_user.id)
    # call verify email endpoint
    email_verifications_api.verify_email(test_client, db_email_verification.verification_code)
    # assert user is verified
    user = users_admin_api.get_user(test_client, logged_in_unverified_user.id)
    assert user.is_verified == True