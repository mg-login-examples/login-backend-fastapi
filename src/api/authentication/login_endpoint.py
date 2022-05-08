import logging

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from data.access_tokens_store.access_token_manager import AccessTokenManager
from helpers.classes.oauth2_password_request_form_extended import OAuth2PasswordRequestFormExtended

from data.schemas.login.login_response import LoginResponse
from crud_endpoints_generator import crud_base
from data.database.models.user import User as UserModel
from utils.security.password_utils import verify_password
from utils.security.access_token_utils import generate_access_token

logger = logging.getLogger(__name__)

def generate_endpoint(
    router: APIRouter,
    db_as_dependency: Session,
    access_token_manager: AccessTokenManager
):
    @router.post("/login/", response_model=LoginResponse)
    def login_user(
        response: Response,
        form_data: OAuth2PasswordRequestFormExtended = Depends(),
        db: Session = db_as_dependency
    ):
        user = crud_base.get_resource_item_by_attribute(db, UserModel, UserModel.email, form_data.username)
        try:
            if user and verify_password(form_data.password, user.hashed_password):
                token_expiry_seconds = 30*24*60*60 if form_data.remember_me else 24*60*60
                access_token = generate_access_token(user.id, token_expiry_seconds)
                if form_data.remember_me:
                    response.set_cookie(key="Authorization", value=f"Bearer {access_token}", httponly=True, expires=token_expiry_seconds)
                else:
                    response.set_cookie(key="Authorization", value=f"Bearer {access_token}", httponly=True)
                access_token_manager.add_access_token(user.id, access_token)
                return LoginResponse(
                    id=user.id,
                    email=user.email,
                    access_token=access_token,
                    token_type='bearer'
                )
        except Exception as e:
            logger.error(e)
        raise HTTPException(status_code=401, detail="Incorrect login")
