from fastapi import BackgroundTasks, status, Response
from sqlalchemy.orm import Session

from helpers_classes.custom_api_router import APIRouter
from data.schemas.users.user import User
from .email_verification_task import create_verification_code_and_send_email


def generate_endpoint(
    router: APIRouter,
    sql_db_session_as_dependency: Session,
    current_user_dependency: User
):
    @router.post("/resend-email/", status_code=status.HTTP_204_NO_CONTENT)
    def resend_verification_email(
        background_tasks: BackgroundTasks,
        user: User = current_user_dependency,
        sql_db_session: Session = sql_db_session_as_dependency
    ):
        if not user.is_verified:
            create_verification_code_and_send_email(
                background_tasks, sql_db_session, user)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
