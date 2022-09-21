from datetime import datetime

from fastapi import BackgroundTasks, status, Response, Request, HTTPException
from sqlalchemy.orm import Session

from stores.sql_db_store import crud_base
from helpers_classes.custom_api_router import APIRouter
from data.database.models.user_password_reset_token import UserPasswordResetToken as UserPasswordResetTokenModel
from data.schemas.user_password_reset_tokens.userPasswordResetToken import UserPasswordResetToken as UserPasswordResetTokenSchema
from data.schemas.authentication.user_password_reset import UserPasswordReset
from data.database.models.user import User as UserModel

from utils.security.password_utils import get_password_hash

# TODO Invalidate all existing access tokens

def generate_endpoint(
    router: APIRouter,
    db_as_dependency: Session
):
    @router.post("/password-reset/", status_code=status.HTTP_204_NO_CONTENT)
    def reset_password(
        background_tasks: BackgroundTasks,
        user_password_change: UserPasswordReset,
        request: Request,
        db: Session = db_as_dependency,
    ):
        token_db_item = crud_base.get_resource_item_by_attribute(db, UserPasswordResetTokenModel, UserPasswordResetTokenModel.token, user_password_change.token)
        if token_db_item:
            token_item = UserPasswordResetTokenSchema(**token_db_item.__dict__)
            if token_item.is_active and token_item.expires_at.timestamp() > datetime.now().timestamp():
                user = crud_base.get_resource_item(db, UserModel, token_item.user_id)
                if user and user.email == user_password_change.email:
                    user.hashed_password = get_password_hash(user_password_change.password)
                    crud_base.update_resource_item_partial(db, UserModel, user)
                    token_item.is_active = False
                    crud_base.update_resource_item_partial(db, UserPasswordResetTokenModel, token_item)
                    return Response(status_code=status.HTTP_204_NO_CONTENT)
        raise HTTPException(status_code=401, detail="Invalid link")
