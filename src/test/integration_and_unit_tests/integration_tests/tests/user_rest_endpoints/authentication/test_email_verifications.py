import logging
from test.integration_and_unit_tests.utils.admin_api import \
    users as users_admin_api
from test.integration_and_unit_tests.utils.user_api import \
    email_verifications as email_verifications_api
from unittest.mock import ANY, MagicMock, patch

import requests  # type: ignore

from data.database.models.user_email_verification import \
    UserEmailVerification as UserEmailVerificationModel
from data.schemas.users.user import User
from stores.sql_db_store import crud_base
from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager
from utils.email.email_utils import send_email

logger = logging.getLogger(__name__)


@patch("fastapi.BackgroundTasks.add_task")
def test_resend_email_unverified_user(
    mock_add_task: MagicMock,
    logged_in_unverified_user: User,
    test_client: requests.Session,
    app_db_manager: SQLAlchemyDBManager,
):
    # assert user is not verified
    assert logged_in_unverified_user.is_verified == False
    # assert no email verifications exist for user
    db_session_1 = next(app_db_manager.db_session())
    db_email_verifications = crud_base.get_resource_items_by_attribute(
        db_session_1,
        UserEmailVerificationModel,
        UserEmailVerificationModel.user_id,
        logged_in_unverified_user.id,
    )
    assert len(db_email_verifications) == 0

    # call send email verification endpoint
    email_verifications_api.resend_verification_email(test_client)

    # assert email verification record exists in db
    db_session_2 = next(app_db_manager.db_session())
    db_email_verifications = crud_base.get_resource_items_by_attribute(
        db_session_2,
        UserEmailVerificationModel,
        UserEmailVerificationModel.user_id,
        logged_in_unverified_user.id,
    )
    assert len(db_email_verifications) == 1
    # assert (mocked) backgroud_tasks.add_task is called
    mock_add_task.assert_called_once_with(
        send_email, logged_in_unverified_user.email, ANY, ANY
    )
    # assert sent email message contains verification code
    email_message = mock_add_task.mock_calls[0].args[3]
    verification_code = db_email_verifications[0].verification_code
    assert str(verification_code) in email_message


@patch("fastapi.BackgroundTasks.add_task")
def test_resend_email_verified_user(
    mock_add_task: MagicMock,
    test_client_logged_in: requests.Session,
    logged_in_user: User,
    app_db_manager: SQLAlchemyDBManager,
):
    # assert user is verified
    assert logged_in_user.is_verified == True
    # assert no email verifications record exist for user in db
    db_session_1 = next(app_db_manager.db_session())
    db_email_verifications = crud_base.get_resource_items_by_attribute(
        db_session_1,
        UserEmailVerificationModel,
        UserEmailVerificationModel.user_id,
        logged_in_user.id,
    )
    assert len(db_email_verifications) == 0

    # call send email verification endpoint
    email_verifications_api.resend_verification_email(test_client_logged_in)

    # assert (mocked) send email function is not called
    mock_add_task.assert_not_called()
    # assert no email verifications record exist for user in db
    db_session_2 = next(app_db_manager.db_session())
    db_email_verifications = crud_base.get_resource_items_by_attribute(
        db_session_2,
        UserEmailVerificationModel,
        UserEmailVerificationModel.user_id,
        logged_in_user.id,
    )
    assert len(db_email_verifications) == 0


@patch("fastapi.BackgroundTasks.add_task")
def test_verify_email(
    mock_add_task: MagicMock,
    logged_in_unverified_user: User,
    test_client: requests.Session,
    app_db_manager: SQLAlchemyDBManager,
):
    # call send email verification endpoint to create a verification code
    # record in db
    email_verifications_api.resend_verification_email(test_client)
    # assert user is unverified
    user = users_admin_api.get_user(test_client, logged_in_unverified_user.id)
    assert user.is_verified == False
    # retrieve verification code from db
    db_session = next(app_db_manager.db_session())
    db_email_verification = crud_base.get_resource_item_by_attribute(
        db_session,
        UserEmailVerificationModel,
        UserEmailVerificationModel.user_id,
        logged_in_unverified_user.id,
    )
    # call verify email endpoint
    email_verifications_api.verify_email(
        test_client, db_email_verification.verification_code
    )
    # assert user is verified
    user = users_admin_api.get_user(test_client, logged_in_unverified_user.id)
    assert user.is_verified == True
