from datetime import datetime

from fastapi import BackgroundTasks, Request, Response, status
from sqlalchemy.orm import Session

from data.database.models.user import User as UserModel
from data.database.models.user_password_reset_token import (
    UserPasswordResetToken as UserPasswordResetTokenModel,
)
from data.schemas.authentication.user_password_reset import UserPasswordReset
from data.schemas.http_error_exceptions.http_400_exceptions import (
    HTTP_400_BAD_REQUEST_EXCEPTION,
)
from data.schemas.http_error_exceptions.http_410_exceptions import (
    HTTP_410_EXPIRED_OR_INACTIVE_CODE_EXCEPTION,
)
from data.schemas.user_password_reset_tokens.userPasswordResetToken import (
    UserPasswordResetToken as UserPasswordResetTokenSchema,
)
from helpers_classes.custom_api_router import APIRouter
from stores.sql_db_store import crud_base
from utils.security.password_utils import get_password_hash

# TODO Invalidate all existing access tokens
# TODO Check password meets requirements


def generate_endpoint(router: APIRouter, sql_db_session_as_dependency: Session):
    @router.post("/password-reset/", status_code=status.HTTP_204_NO_CONTENT)
    def reset_password(
        background_tasks: BackgroundTasks,
        user_password_change: UserPasswordReset,
        request: Request,
        sql_db_session: Session = sql_db_session_as_dependency,
    ):
        token_db_item = crud_base.get_resource_item_by_attribute(
            sql_db_session,
            UserPasswordResetTokenModel,
            UserPasswordResetTokenModel.token,
            user_password_change.token,
        )
        if not token_db_item:
            raise HTTP_400_BAD_REQUEST_EXCEPTION
        token_item = UserPasswordResetTokenSchema(**token_db_item.__dict__)
        if (not token_item.is_active) or (
            datetime.now().timestamp() > token_item.expires_at.timestamp()
        ):
            raise HTTP_410_EXPIRED_OR_INACTIVE_CODE_EXCEPTION
        user = crud_base.get_resource_item(
            sql_db_session, UserModel, token_item.user_id
        )
        if (not user) or (user.email != user_password_change.email):
            raise HTTP_400_BAD_REQUEST_EXCEPTION
        user.hashed_password = get_password_hash(user_password_change.password)
        crud_base.update_resource_item_partial(sql_db_session, UserModel, user)
        token_item.is_active = False
        crud_base.update_resource_item_partial(
            sql_db_session, UserPasswordResetTokenModel, token_item
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
