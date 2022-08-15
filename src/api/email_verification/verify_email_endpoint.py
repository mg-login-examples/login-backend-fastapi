from fastapi import HTTPException, status, Response
from sqlalchemy.orm import Session
from datetime import datetime

from api_dependencies.helper_classes.custom_api_router import APIRouter
from crud_endpoints_generator import crud_base
from data.database.models.user import User as UserModel
from data.schemas.users.user import User
from data.database.models.user_email_verification import UserEmailVerification as UserEmailVerificationModel
from data.schemas.user_email_verifications.userEmailVerification import UserEmailVerification as UserEmailVerificationSchema

def generate_endpoint(
    router: APIRouter,
    db_as_dependency: Session,
    current_user_dependency: User
):
    @router.post("/verify-email/{verification_code}/", status_code=status.HTTP_204_NO_CONTENT)
    def verify_email(
        verification_code: int,
        user: User = current_user_dependency,
        db: Session = db_as_dependency,
        status_code=status.HTTP_204_NO_CONTENT
    ):
        queryFiltersAndValues = [
            (UserEmailVerificationModel.user_id, user.id),
            (UserEmailVerificationModel.verification_code, verification_code)
        ]
        db_email_verification = crud_base.get_resource_item_by_attributes(db, UserEmailVerificationModel, queryFiltersAndValues)
        if db_email_verification and db_email_verification.expires_at.timestamp() > datetime.utcnow().timestamp():
            user.is_verified = True
            crud_base.update_resource_item_partial(db, UserModel, user)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        raise HTTPException(status_code=404, detail="Incorrect verification code")
