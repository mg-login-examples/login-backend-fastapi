from fastapi import BackgroundTasks, status, Response
from sqlalchemy.orm import Session

from api_dependencies.helper_classes.custom_api_router import APIRouter
from data.schemas.users.user import User
from background_tasks.emails import send_verification_email_task

def generate_endpoint(
    router: APIRouter,
    db_as_dependency: Session,
    current_user_dependency: User
):
    @router.post("/resend-email/", status_code=status.HTTP_204_NO_CONTENT)
    def resend_verification_email_endpoint(
        background_tasks: BackgroundTasks,
        user: User = current_user_dependency,
        db: Session = db_as_dependency
    ):
        if not user.is_verified:
            background_tasks.add_task(send_verification_email_task, db, user.id, user.email)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
