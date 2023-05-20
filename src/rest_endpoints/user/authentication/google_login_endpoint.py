import logging
from datetime import datetime

from fastapi import APIRouter, HTTPException, Response
from fastapi.requests import Request
from fastapi.security.utils import get_authorization_scheme_param
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests

from helpers_classes.custom_api_router import APIRouter
from stores.access_tokens_store.access_token_store import AccessTokenStore
from data.schemas.authentication.google_sign_in_payload import GoogleSignInPayload
from data.schemas.authentication.login_response import LoginResponse
from stores.sql_db_store import crud_base
from data.database.models.user import User as UserModel
from data.schemas.users.userBase import UserBase
from data.schemas.users.user import User
from data.database.models.user_session import UserSession as UserSessionModel
from data.schemas.user_sessions.userSessionCreate import UserSessionCreate
from utils.security.access_token_utils import generate_access_token
from utils.security.auth_cookies import add_authorization_cookie_to_response

logger = logging.getLogger(__name__)

# TODO Move to environment variable or secrets if needed
google_client_id = "94297494812-duhngd0ecimur6q39gd1l5qbdfnced4p.apps.googleusercontent.com"

def generate_endpoint(
    router: APIRouter,
    db_as_dependency: Session,
    access_token_store_as_dependency: AccessTokenStore,
    auth_cookie_type: str,
):
    @router.post("/oauth/google", response_model=LoginResponse)
    async def google_login(
        request: Request,
        response: Response,
        google_sign_in_payload: GoogleSignInPayload,
        db: Session = db_as_dependency,
        access_token_store: AccessTokenStore = access_token_store_as_dependency
    ):
        try:
            idinfo = id_token.verify_oauth2_token(google_sign_in_payload.credential, requests.Request(), google_client_id)
            user_email = idinfo["email"]
            user = crud_base.get_resource_item_by_attribute(db, UserModel, UserModel.email, user_email)
            if not user and idinfo["email_verified"] == True:
                logger.info("Creating new user")
                user_to_create = UserBase(email=user_email)
                user_db = crud_base.create_resource_item(db, UserModel, user_to_create)
                user = User(**user_db.__dict__)
                user.is_verified = True
                if idinfo["name"]:
                    user.name = idinfo["name"]
                # TODO Download user profile idinfo["picture"], save it locally and add profile link
                crud_base.update_resource_item_full(db, UserModel, user)

            if user:
                token_expiry_duration_seconds = 30*24*60*60
                token_expiry_datetime_timestamp = int(datetime.now().timestamp()) + token_expiry_duration_seconds
                access_token = generate_access_token(user.id, token_expiry_datetime_timestamp)

                userSession = UserSessionCreate(user_id=user.id, token=access_token, expires_at=datetime.fromtimestamp(token_expiry_datetime_timestamp))
                crud_base.create_resource_item(db, UserSessionModel, userSession)
                await access_token_store.add_access_token(user.id, access_token)

                # Delete existing access token if any
                cookie_authorization: str = request.cookies.get("Authorization")
                _, cookie_param = get_authorization_scheme_param(
                    cookie_authorization
                )
                if cookie_param:
                    previous_access_token = cookie_param
                    crud_base.delete_resource_item_by_attribute(db, UserSessionModel, UserSessionModel.token, previous_access_token)

                add_authorization_cookie_to_response(response, auth_cookie_type, "Authorization", f"Bearer {access_token}", None)

                return LoginResponse(
                    user=user,
                    access_token=access_token,
                    token_type='bearer'
                )
        except Exception as e:
            logger.error(e)
        logger.error(f"Unsuccessful google user login")
        raise HTTPException(status_code=401, detail="Incorrect login")
