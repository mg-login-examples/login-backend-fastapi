from fastapi import BackgroundTasks, Request, Response, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from data.database.models.user import User as UserModel
from helpers_classes.custom_api_router import APIRouter
from stores.sql_db_store import crud_base

from .password_reset_link_task import create_password_reset_link_and_send_email


def generate_endpoint(router: APIRouter, sql_db_session_as_dependency: Session):

    class UserEmail(BaseModel):
        email: EmailStr

    @router.post("/password-reset-link/", status_code=status.HTTP_204_NO_CONTENT)
    def send_password_reset_link_email(
        background_tasks: BackgroundTasks,
        user_email: UserEmail,
        request: Request,
        sql_db_session: Session = sql_db_session_as_dependency,
    ):
        user = crud_base.get_resource_item_by_attribute(
            sql_db_session, UserModel, UserModel.email, user_email.email
        )
        if user:
            create_password_reset_link_and_send_email(
                background_tasks, sql_db_session, user, str(request.base_url)
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
