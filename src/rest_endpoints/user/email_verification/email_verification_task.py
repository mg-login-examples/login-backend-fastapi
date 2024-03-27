from random import randint
from datetime import datetime, timedelta

from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from data.schemas.users.user import User
from stores.sql_db_store import crud_base
from data.database.models.user_email_verification import UserEmailVerification as UserEmailVerificationModel
from data.schemas.user_email_verifications.userEmailVerificationBase import UserEmailVerificationBase as UserEmailVerificationSchema
from utils.email.email_utils import send_email


def create_verification_code_and_send_email(
        background_tasks: BackgroundTasks, sql_db_session: Session, user: User):
    verification_code = randint(100000, 999999)
    expires_at = datetime.now() + timedelta(hours=24)
    user_email_verification = UserEmailVerificationSchema(
        verification_code=verification_code,
        user_id=user.id,
        expires_at=expires_at
    )
    crud_base.create_resource_item(
        sql_db_session,
        UserEmailVerificationModel,
        user_email_verification
    )

    receiver_email_address = user.email
    email_subject = "Email Verification"
    email_message = (
        "Please enter the following code on the email verification page: \n"
        f"{verification_code}\n\n"
        "Note: This code will expire in 24 hours."
    )
    background_tasks.add_task(
        send_email, receiver_email_address, email_subject, email_message)
