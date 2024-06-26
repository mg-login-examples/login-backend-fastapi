import logging
from datetime import datetime

from fastapi import APIRouter, Depends, Response
from fastapi.requests import Request
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.orm import Session

from data.database.models.user import User as UserModel
from data.database.models.user_session import UserSession as UserSessionModel
from data.schemas.authentication.login_response import LoginResponse
from data.schemas.http_error_exceptions.http_401_exceptions import (
    HTTP_401_INVALID_LOGIN_EXCEPTION,
)
from data.schemas.user_sessions.userSessionCreate import UserSessionCreate
from helpers_classes.custom_api_router import APIRouter
from helpers_classes.oauth2_password_request_form_extended import (
    OAuth2PasswordRequestFormExtended,
)
from stores.access_tokens_store.access_token_store import AccessTokenStore
from stores.sql_db_store import crud_base
from utils.security.access_token_utils import generate_access_token
from utils.security.auth_cookies import add_authorization_cookie_to_response
from utils.security.password_utils import verify_password

logger = logging.getLogger(__name__)


def generate_endpoint(
    router: APIRouter,
    sql_db_session_as_dependency: Session,
    access_token_store_as_dependency: AccessTokenStore,
    auth_cookie_type: str,
):
    @router.post("/login/", response_model=LoginResponse)
    async def login_user(
        request: Request,
        response: Response,
        form_data: OAuth2PasswordRequestFormExtended = Depends(),
        sql_db_session: Session = sql_db_session_as_dependency,
        access_token_store: AccessTokenStore = access_token_store_as_dependency,
    ):
        user = crud_base.get_resource_item_by_attribute(
            sql_db_session, UserModel, UserModel.email, form_data.username
        )
        try:
            if user and verify_password(form_data.password, user.hashed_password):
                token_expiry_duration_seconds = (
                    30 * 24 * 60 * 60 if form_data.remember_me else 24 * 60 * 60
                )
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

                # Delete existing access token if any
                cookie_authorization = request.cookies.get("Authorization")
                _, cookie_param = get_authorization_scheme_param(cookie_authorization)
                if cookie_param:
                    previous_access_token = cookie_param
                    crud_base.delete_resource_item_by_attribute(
                        sql_db_session,
                        UserSessionModel,
                        UserSessionModel.token,
                        previous_access_token,
                    )

                if form_data.remember_me:
                    add_authorization_cookie_to_response(
                        response,
                        auth_cookie_type,
                        "Authorization",
                        f"Bearer {access_token}",
                        token_expiry_duration_seconds,
                    )
                else:
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
        logger.error(f"Unsuccessful user login with username: {form_data.username}")
        raise HTTP_401_INVALID_LOGIN_EXCEPTION
