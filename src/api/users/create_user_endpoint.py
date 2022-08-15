from fastapi import BackgroundTasks, Response
from sqlalchemy.orm import Session

from api_dependencies.helper_classes.custom_api_router import APIRouter
from crud_endpoints_generator import crud_base
from data.database.models.user import User as UserModel
from data.schemas.users.userCreate import UserCreate
from data.endUserSchemasToDbSchemas.user import createSchemaToDbSchema as userCreateSchemaToDbSchema
from utils.security.access_token_utils import generate_access_token
from data.access_tokens_store.access_token_manager import AccessTokenManager
from background_tasks.emails import send_verification_email_task
from data.schemas.login.login_response import LoginResponse


def generate_endpoint(
    router: APIRouter,
    db_as_dependency: Session,
    access_token_manager: AccessTokenManager,
    samesite: str,
    secure_cookies: bool
):
    @router.post("/", response_model=LoginResponse)
    def create_user(
        response: Response,
        user: UserCreate,
        background_tasks: BackgroundTasks,
        db: Session = db_as_dependency,
    ):
        user_with_password_hash = userCreateSchemaToDbSchema(user)
        user_db = crud_base.create_resource_item(db, UserModel, user_with_password_hash)

        token_expiry_seconds = 24*60*60
        access_token = generate_access_token(user_db.id, token_expiry_seconds)
        response.set_cookie(key="Authorization", value=f"Bearer {access_token}", httponly=True, samesite=samesite, secure=secure_cookies)
        access_token_manager.add_access_token(user_db.id, access_token)

        background_tasks.add_task(send_verification_email_task, db, user_db.id, user_db.email)

        return LoginResponse(
            user=user_db,
            access_token=access_token,
            token_type='bearer'
        )
