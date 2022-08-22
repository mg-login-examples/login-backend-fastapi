from fastapi import BackgroundTasks, status, Response, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from crud_endpoints_generator import crud_base
from api_dependencies.helper_classes.custom_api_router import APIRouter
from data.database.models.user import User as UserModel
from api.authentication.password_reset_link_task import create_password_reset_link_and_send_email

def generate_endpoint(
    router: APIRouter,
    db_as_dependency: Session
):

    class UserEmail(BaseModel):
        email: EmailStr

    @router.post("/password-reset-link/", status_code=status.HTTP_204_NO_CONTENT)
    def send_password_reset_link_email(
        background_tasks: BackgroundTasks,
        user_email: UserEmail,
        request: Request,
        db: Session = db_as_dependency,
    ):
        user = crud_base.get_resource_item_by_attribute(db, UserModel, UserModel.email, user_email.email)
        if user:
            create_password_reset_link_and_send_email(background_tasks, db, user, request.base_url)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
