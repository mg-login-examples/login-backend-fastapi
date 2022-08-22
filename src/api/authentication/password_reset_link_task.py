from datetime import datetime, timedelta
import secrets

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from data.schemas.users.user import User
from crud_endpoints_generator import crud_base
from data.database.models.user_password_reset_token import UserPasswordResetToken as UserPasswordResetTokenModel
from data.schemas.user_password_reset_tokens.userPasswordResetTokenBase import UserPasswordResetTokenBase as UserPasswordResetTokenSchema
from utils.email.email_utils import send_email

def create_password_reset_link_and_send_email(background_tasks: BackgroundTasks, db: Session, user: User, app_base_url: str):
    reset_password_token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours = 2)
    user_password_reset_token = UserPasswordResetTokenSchema(
        token=reset_password_token,
        user_id=user.id,
        expires_at=expires_at,
        is_active=True,
    )
    crud_base.create_resource_item(
        db,
        UserPasswordResetTokenModel,
        user_password_reset_token
    )

    link = f"{app_base_url}password-reset?email={user.email}&token={reset_password_token}"
    receiver_email_address = user.email
    email_subject = "Reset Password"
    email_message = (
        "Please click on this link to reset your password: \n"
        f"{link}\n\n"
        "Note: This link will expire in 2 hours."
    )
    background_tasks.add_task(send_email, receiver_email_address, email_subject, email_message)
