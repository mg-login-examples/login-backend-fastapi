from datetime import datetime

from fastapi import BackgroundTasks, status, Response, Request, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from crud_endpoints_generator import crud_base
from api_dependencies.helper_classes.custom_api_router import APIRouter
from data.database.models.user_password_reset_token import UserPasswordResetToken as UserPasswordResetTokenModel
from data.schemas.user_password_reset_tokens.userPasswordResetToken import UserPasswordResetToken as UserPasswordResetTokenSchema
from data.database.models.user import User as UserModel
from api.authentication.password_reset_link_task import create_password_reset_link_and_send_email
from utils.security.password_utils import get_password_hash

def generate_endpoint(
    router: APIRouter,
    db_as_dependency: Session
):

    class UserPasswordChange(BaseModel):
        email: EmailStr
        password: str
        token: str

    @router.post("/password-reset/", status_code=status.HTTP_204_NO_CONTENT)
    def reset_password(
        background_tasks: BackgroundTasks,
        user_password_change: UserPasswordChange,
        request: Request,
        db: Session = db_as_dependency,
    ):
        token_db_item = crud_base.get_resource_item_by_attribute(db, UserPasswordResetTokenModel, UserPasswordResetTokenModel.token, user_password_change.token)
        if token_db_item:
            token_item = UserPasswordResetTokenSchema(**token_db_item.__dict__)
            if token_item.is_active and token_item.expires_at.timestamp() > datetime.utcnow().timestamp():
                user = crud_base.get_resource_item(db, UserModel, token_item.user_id)
                if user and user.email == user_password_change.email:
                    hashed_password = get_password_hash(user_password_change.password)
                    user.password = hashed_password
                    crud_base.update_resource_item_partial(db, UserModel, user)
                    token_item.is_active = False
                    crud_base.update_resource_item_partial(db, UserPasswordResetTokenModel, token_item)
                    return Response(status_code=status.HTTP_204_NO_CONTENT)
        raise HTTPException(status_code=401, detail="Invalid token")
