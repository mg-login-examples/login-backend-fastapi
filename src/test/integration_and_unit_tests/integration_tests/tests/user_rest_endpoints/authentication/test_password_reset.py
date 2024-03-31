import logging
from unittest.mock import MagicMock, patch, ANY

import requests  # type: ignore

from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager
from stores.sql_db_store import crud_base
from data.database.models.user_password_reset_token import UserPasswordResetToken as UserPasswordResetTokenModel
from data.schemas.users.userCreate import UserCreate
from data.schemas.users.userDeep import User as UserDeep
from test.integration_and_unit_tests.utils.user_api import password_reset as password_reset_api
from test.integration_and_unit_tests.utils.user_api import authentication as authentication_api
from utils.email.email_utils import send_email

logger = logging.getLogger(__name__)


@patch("fastapi.BackgroundTasks.add_task")
def test_password_reset_link_valid_email(mock_add_task: MagicMock, created_user_by_admin: UserDeep,
                                         test_client: requests.Session, app_db_manager: SQLAlchemyDBManager):
    # assert no password reset token exist for user
    db_session_1 = next(app_db_manager.db_session())
    db_password_reset_tokens = crud_base.get_resource_items_by_attribute(
        db_session_1, UserPasswordResetTokenModel, UserPasswordResetTokenModel.user_id, created_user_by_admin.id)
    assert len(db_password_reset_tokens) == 0

    # call generate link to reset password endpoint
    password_reset_api.generate_password_reset_link(
        test_client, created_user_by_admin.email)

    # assert password reset token record exists in db
    db_session_2 = next(app_db_manager.db_session())
    db_password_reset_tokens = crud_base.get_resource_items_by_attribute(
        db_session_2, UserPasswordResetTokenModel, UserPasswordResetTokenModel.user_id, created_user_by_admin.id)
    assert len(db_password_reset_tokens) == 1
    # assert (mocked) backgroud_tasks.add_task is called
    mock_add_task.assert_called_once_with(
        send_email, created_user_by_admin.email, ANY, ANY)
    # assert sent email message contains reset password link
    email_message = mock_add_task.mock_calls[0].args[3]
    token = db_password_reset_tokens[0].token
    expires_at_timestamp = db_password_reset_tokens[0].expires_at.timestamp()
    expected_link = f"{test_client.base_url}/password-reset?email={
        created_user_by_admin.email}&token={token}&expires_at={expires_at_timestamp}"
    assert expected_link in email_message


@patch("fastapi.BackgroundTasks.add_task")
def test_reset_password(mock_add_task: MagicMock, user_login: UserCreate, created_user_by_admin: UserDeep,
                        test_client: requests.Session, app_db_manager: SQLAlchemyDBManager):
    # call generate password reset link endpoint to create a password reset
    # token record in db
    password_reset_api.generate_password_reset_link(
        test_client, created_user_by_admin.email)
    # retrieve password reset token from db
    db_session = next(app_db_manager.db_session())
    db_password_reset_token = crud_base.get_resource_item_by_attribute(
        db_session, UserPasswordResetTokenModel, UserPasswordResetTokenModel.user_id, created_user_by_admin.id)
    # call verify email endpoint
    new_password = "asdkj3234sadf"
    password_reset_api.reset_password(
        test_client, created_user_by_admin.email, new_password, db_password_reset_token.token)
    # assert user login with new password is successful
    new_user_login = UserCreate(email=user_login.email, password=new_password)
    loginResponse = authentication_api.login(test_client, new_user_login)
    assert loginResponse.user.id == created_user_by_admin.id
    # assert user login with old password is unsuccessful
    authentication_api.login_expect_unauthorized(test_client, user_login)


@patch("fastapi.BackgroundTasks.add_task")
def test_reset_password_token_deactivated_after_reset_password_is_called(
        mock_add_task: MagicMock, user_login: UserCreate, created_user_by_admin: UserDeep, test_client: requests.Session, app_db_manager: SQLAlchemyDBManager):
    # call generate password reset link endpoint to create a password reset
    # token record in db
    password_reset_api.generate_password_reset_link(
        test_client, created_user_by_admin.email)
    # retrieve password reset token from db
    db_session_1 = next(app_db_manager.db_session())
    db_password_reset_token = crud_base.get_resource_item_by_attribute(
        db_session_1, UserPasswordResetTokenModel, UserPasswordResetTokenModel.user_id, created_user_by_admin.id)
    assert db_password_reset_token.is_active == True
    # call verify email endpoint
    new_password = "faafasdfaoioi"
    password_reset_api.reset_password(
        test_client, created_user_by_admin.email, new_password, db_password_reset_token.token)
    # assert password token is deactivated
    db_session_2 = next(app_db_manager.db_session())
    db_password_reset_token = crud_base.get_resource_item_by_attribute(
        db_session_2, UserPasswordResetTokenModel, UserPasswordResetTokenModel.user_id, created_user_by_admin.id)
    assert db_password_reset_token.is_active == False
    new_password = "asdfaoposd"
    password_reset_api.reset_password_expect_unauthorized(
        test_client, created_user_by_admin.email, new_password, db_password_reset_token.token)
