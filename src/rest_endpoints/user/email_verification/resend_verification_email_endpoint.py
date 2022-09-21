from fastapi import BackgroundTasks, status, Response
from sqlalchemy.orm import Session

from helpers_classes.custom_api_router import APIRouter
from data.schemas.users.user import User
from .email_verification_task import create_verification_code_and_send_email

def generate_endpoint(
    router: APIRouter,
    db_as_dependency: Session,
    current_user_dependency: User
):
    @router.post("/resend-email/", status_code=status.HTTP_204_NO_CONTENT)
    def resend_verification_email(
        background_tasks: BackgroundTasks,
        user: User = current_user_dependency,
        db: Session = db_as_dependency
    ):
        if not user.is_verified:
            create_verification_code_and_send_email(background_tasks, db, user)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
