from datetime import datetime

from fastapi import BackgroundTasks, Response
from sqlalchemy.orm import Session

from helpers_classes.custom_api_router import APIRouter
from stores.sql_db_store import crud_base
from data.database.models.user import User as UserModel
from data.schemas.users.userCreate import UserCreate
from data.endUserSchemasToDbSchemas.user import (
    createSchemaToDbSchema as userCreateSchemaToDbSchema,
)
from utils.security.access_token_utils import generate_access_token
from stores.access_tokens_store.access_token_store import AccessTokenStore
from data.schemas.authentication.login_response import LoginResponse
from data.schemas.users.user import User
from data.database.models.user_session import UserSession as UserSessionModel
from data.schemas.user_sessions.userSessionCreate import UserSessionCreate
from rest_endpoints.user.email_verification.email_verification_task import (
    create_verification_code_and_send_email,
)
from utils.security.auth_cookies import add_authorization_cookie_to_response


def generate_endpoint(
    router: APIRouter,
    sql_db_session_as_dependency: Session,
    access_token_store_as_dependency: AccessTokenStore,
    auth_cookie_type: str,
):
    @router.post("/", response_model=LoginResponse)
    async def create_user(
        response: Response,
        user: UserCreate,
        background_tasks: BackgroundTasks,
        sql_db_session: Session = sql_db_session_as_dependency,
        access_token_store: AccessTokenStore = access_token_store_as_dependency,
    ):
        user_with_password_hash = userCreateSchemaToDbSchema(user)
        user_db = crud_base.create_resource_item(
            sql_db_session, UserModel, user_with_password_hash
        )
        user_schema = User(**user_db.__dict__)

        token_expiry_duration_seconds = 24 * 60 * 60
        token_expiry_datetime_timestamp = (
            int(datetime.now().timestamp()) + token_expiry_duration_seconds
        )
        access_token = generate_access_token(
            user_schema.id, token_expiry_datetime_timestamp
        )

        userSession = UserSessionCreate(
            user_id=user_schema.id,
            token=access_token,
            expires_at=datetime.fromtimestamp(token_expiry_datetime_timestamp),
        )
        crud_base.create_resource_item(sql_db_session, UserSessionModel, userSession)
        await access_token_store.add_access_token(user_db.id, access_token)

        create_verification_code_and_send_email(
            background_tasks, sql_db_session, user_schema
        )

        add_authorization_cookie_to_response(
            response, auth_cookie_type, "Authorization", f"Bearer {access_token}", None
        )

        return LoginResponse(
            user=user_db, access_token=access_token, token_type="bearer"
        )
