from typing import List

from sqlalchemy.orm import Session

from api_dependencies.helper_classes.custom_api_router import APIRouter
from crud_endpoints_generator import crud_base
from data.schemas.users.user import User
from data.database.models.user_session import UserSession as UserSessionModel
from data.schemas.user_sessions.userSession import UserSession as UserSessionSchema

def generate_endpoint(
    router: APIRouter,
    db_as_dependency: Session,
    current_user_as_dependency: User
):
    @router.get("/{user_id}/sessions/", response_model=List[UserSessionSchema], dependencies=[current_user_as_dependency])
    def get_user_quotes(
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        db: Session = db_as_dependency
    ):
        userSessions = crud_base.get_resource_items_by_attribute(db, UserSessionModel, UserSessionModel.user_id, user_id, skip=skip, limit=limit)
        return userSessions
