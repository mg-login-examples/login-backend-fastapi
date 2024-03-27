from datetime import datetime
import logging

from fastapi import status, Response
from sqlalchemy.orm import Session

from helpers_classes.custom_api_router import APIRouter
from stores.sql_db_store import crud_base
from data.database.models.user import User as UserModel
from data.schemas.users.user import User
from data.database.models.user_email_verification import UserEmailVerification as UserEmailVerificationModel
from data.schemas.http_error_exceptions.http_401_exceptions import HTTP_401_INCORRECT_VERIFICATION_CODE_EXCEPTION
from data.schemas.http_error_exceptions.http_500_exceptions import HTTP_500_UNEXPECTED_EXCEPTION

logger = logging.getLogger(__name__)


def generate_endpoint(
    router: APIRouter,
    sql_db_session_as_dependency: Session,
    current_user_dependency: User
):
    @router.post("/verify-email/{verification_code}/",
                 status_code=status.HTTP_204_NO_CONTENT)
    def verify_email(
        verification_code: int,
        user: User = current_user_dependency,
        sql_db_session: Session = sql_db_session_as_dependency
    ):
        try:
            queryFiltersAndValues = [
                (UserEmailVerificationModel.user_id, user.id),
                (UserEmailVerificationModel.verification_code, verification_code)
            ]
            db_email_verification = crud_base.get_resource_item_by_attributes(
                sql_db_session, UserEmailVerificationModel, queryFiltersAndValues)
            if db_email_verification and db_email_verification.expires_at.timestamp(
            ) > datetime.now().timestamp():
                user.is_verified = True
                crud_base.update_resource_item_partial(
                    sql_db_session, UserModel, user)
                return Response(status_code=status.HTTP_204_NO_CONTENT)
            raise HTTP_401_INCORRECT_VERIFICATION_CODE_EXCEPTION
        except Exception as e:
            logger.error(e)
            raise HTTP_500_UNEXPECTED_EXCEPTION
