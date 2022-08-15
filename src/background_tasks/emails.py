from sqlalchemy.orm import Session
from random import randint
from datetime import datetime, timedelta

from utils.email.email_utils import send_email
from crud_endpoints_generator import crud_base
from data.database.models.user_email_verification import UserEmailVerification as UserEmailVerificationModel
from data.schemas.user_email_verifications.userEmailVerificationBase import UserEmailVerificationBase as UserEmailVerificationSchema

def send_verification_email_task(db: Session, user_id: int, email: str):
    verification_code = randint(100000, 999999)
    expires_at = datetime.utcnow() + timedelta(hours = 24)
    user_email_verification = UserEmailVerificationSchema(
        verification_code=verification_code,
        user_id=user_id,
        expires_at=expires_at
    )
    db_user_email_verification = crud_base.create_resource_item(
        db,
        UserEmailVerificationModel,
        user_email_verification
    )
    send_email(
        email,
        "Email Verification",
        (
            "Please enter the following code on the email verification page: \n"
            f"{verification_code}\n\n"
            "This code will expire in 24 hours"
        )
    )
