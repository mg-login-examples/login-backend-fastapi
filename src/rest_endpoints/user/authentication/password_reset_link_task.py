from datetime import datetime, timedelta
import secrets

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from data.schemas.users.user import User
from stores.sql_db_store import crud_base
from data.database.models.user_password_reset_token import (
    UserPasswordResetToken as UserPasswordResetTokenModel,
)
from data.schemas.user_password_reset_tokens.userPasswordResetTokenBase import (
    UserPasswordResetTokenBase as UserPasswordResetTokenSchema,
)
from utils.email.email_utils import send_email

import logging

logger = logging.getLogger(__name__)


def create_password_reset_link_and_send_email(
    background_tasks: BackgroundTasks,
    sql_db_session: Session,
    user: User,
    app_base_url: str,
):
    reset_password_token = secrets.token_urlsafe(32)
    expires_at = datetime.now() + timedelta(hours=2)
    user_password_reset_token = UserPasswordResetTokenSchema(
        token=reset_password_token,
        user_id=user.id,
        expires_at=expires_at,
        is_active=True,
    )
    created_token_db_item = crud_base.create_resource_item(
        sql_db_session, UserPasswordResetTokenModel, user_password_reset_token
    )
    # Update expires_at variable as miliseconds are truncated when stored in
    # mysql
    expires_at = created_token_db_item.expires_at

    link = f"{app_base_url}password-reset?email={user.email}&token={reset_password_token}&expires_at={expires_at.timestamp()}"
    receiver_email_address = user.email
    email_subject = "Reset Password"
    email_message = (
        "Please click on this link to reset your password: \n"
        f"{link}\n\n"
        "Note: This link will expire in 2 hours."
    )
    background_tasks.add_task(
        send_email, receiver_email_address, email_subject, email_message
    )
