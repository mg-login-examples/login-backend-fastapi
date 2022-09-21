import logging
from datetime import datetime

from fastapi import Depends, HTTPException, Response
from sqlalchemy.orm import Session

from helpers_classes.custom_api_router import APIRouter
from stores.access_tokens_store.access_token_store import AccessTokenStore
from helpers_classes.oauth2_password_request_form_extended import OAuth2PasswordRequestFormExtended
from data.schemas.admin_login.admin_login_response import AdminLoginResponse
from stores.sql_db_store import crud_base
from data.database.models.admin_user import AdminUser as AdminUserModel
from utils.security.password_utils import verify_password
from utils.security.access_token_utils import generate_access_token

logger = logging.getLogger(__name__)

def generate_endpoint(
    router: APIRouter,
    db_as_dependency: Session,
    access_token_store_as_dependency: AccessTokenStore,
    secure_cookies: bool
):
    @router.post("/login/", response_model=AdminLoginResponse)
    async def login_admin_user(
        response: Response,
        form_data: OAuth2PasswordRequestFormExtended = Depends(),
        db: Session = db_as_dependency,
        access_token_store: AccessTokenStore = access_token_store_as_dependency
    ):
        user = crud_base.get_resource_item_by_attribute(db, AdminUserModel, AdminUserModel.email, form_data.username)
        try:
            if user and verify_password(form_data.password, user.hashed_password):
                token_expiry_duration_seconds = 30*24*60*60 if form_data.remember_me else 24*60*60
                token_expiry_datetime_timestamp = int(datetime.now().timestamp()) + token_expiry_duration_seconds
                access_token = generate_access_token(user.id, token_expiry_datetime_timestamp)

                await access_token_store.add_access_token(user.id, access_token)

                if form_data.remember_me:
                    response.set_cookie(key="Admin-Authorization", value=f"Bearer {access_token}", httponly=True, samesite="strict", secure=secure_cookies, expires=datetime.fromtimestamp(token_expiry_datetime_timestamp))
                else:
                    response.set_cookie(key="Admin-Authorization", value=f"Bearer {access_token}", httponly=True, samesite="strict", secure=secure_cookies)

                return AdminLoginResponse(
                    id=user.id,
                    email=user.email,
                    access_token=access_token,
                    token_type='bearer'
                )
        except Exception as e:
            logger.error(e)
        logger.error(f"Unsuccessful admin login with username: {form_data.username}")
        raise HTTPException(status_code=401, detail="Incorrect login")
