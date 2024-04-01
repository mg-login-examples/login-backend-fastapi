import logging
from datetime import datetime

from fastapi import APIRouter, Response
from sqlalchemy.orm import Session

from helpers_classes.custom_api_router import APIRouter
from stores.access_tokens_store.access_token_store import AccessTokenStore
from data.schemas.authentication.login_response import LoginResponse
from stores.sql_db_store import crud_base
from data.schemas.users.user import User as UserSchema
from data.database.models.user import User as UserModel
from data.database.models.user_session import UserSession as UserSessionModel
from data.schemas.authentication.user_password_change import UserPasswordChange
from data.schemas.user_sessions.userSessionCreate import UserSessionCreate
from utils.security.password_utils import verify_password, get_password_hash
from utils.security.access_token_utils import generate_access_token
from utils.security.auth_cookies import add_authorization_cookie_to_response
from data.schemas.http_error_exceptions.http_400_exceptions import (
    HTTP_400_BAD_REQUEST_EXCEPTION,
    HTTP_400_INVALID_PASSWORD_EXCEPTION,
)
from data.schemas.http_error_exceptions.http_401_exceptions import (
    HTTP_401_INVALID_CREDENTIALS_EXCEPTION,
)
from data.schemas.http_error_exceptions.http_403_exceptions import (
    HTTP_403_NOT_AUTHORIZED_EXCEPTION,
)
from data.schemas.http_error_exceptions.http_500_exceptions import (
    HTTP_500_UNEXPECTED_EXCEPTION,
)

logger = logging.getLogger(__name__)

# TODO Invalidate all existing access tokens


def generate_endpoint(
    router: APIRouter,
    sql_db_session_as_dependency: Session,
    access_token_store_as_dependency: AccessTokenStore,
    get_current_user_as_dependency: UserSchema,
    auth_cookie_type: str,
):
    @router.post("/password-change/", response_model=LoginResponse)
    async def change_user_password(
        response: Response,
        user_password_change: UserPasswordChange,
        current_user: UserSchema = get_current_user_as_dependency,
        sql_db_session: Session = sql_db_session_as_dependency,
        access_token_store: AccessTokenStore = access_token_store_as_dependency,
    ):
        user = crud_base.get_resource_item_by_attribute(
            sql_db_session, UserModel, UserModel.email, user_password_change.username
        )
        try:
            if not user:
                raise HTTP_400_BAD_REQUEST_EXCEPTION
            if user.id != current_user.id:
                raise HTTP_403_NOT_AUTHORIZED_EXCEPTION
            if not verify_password(user_password_change.password, user.hashed_password):
                raise HTTP_401_INVALID_CREDENTIALS_EXCEPTION
            if user_password_change.password == user_password_change.password_new:
                raise HTTP_400_INVALID_PASSWORD_EXCEPTION

            user.hashed_password = get_password_hash(user_password_change.password_new)
            crud_base.update_resource_item_partial(sql_db_session, UserModel, user)

            token_expiry_duration_seconds = 24 * 60 * 60
            token_expiry_datetime_timestamp = (
                int(datetime.now().timestamp()) + token_expiry_duration_seconds
            )
            access_token = generate_access_token(
                user.id, token_expiry_datetime_timestamp
            )

            userSession = UserSessionCreate(
                user_id=user.id,
                token=access_token,
                expires_at=datetime.fromtimestamp(token_expiry_datetime_timestamp),
            )
            crud_base.create_resource_item(
                sql_db_session, UserSessionModel, userSession
            )
            await access_token_store.add_access_token(user.id, access_token)

            add_authorization_cookie_to_response(
                response,
                auth_cookie_type,
                "Authorization",
                f"Bearer {access_token}",
                None,
            )

            return LoginResponse(
                user=user, access_token=access_token, token_type="bearer"
            )
        except Exception as e:
            logger.error(e)
            raise HTTP_500_UNEXPECTED_EXCEPTION
