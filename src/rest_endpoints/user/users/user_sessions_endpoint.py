from typing import Any

from sqlalchemy.orm import Session

from helpers_classes.custom_api_router import APIRouter
from stores.sql_db_store import crud_base
from data.database.models.user_session import UserSession as UserSessionModel
from data.schemas.user_sessions.userSession import UserSession as UserSessionSchema

def generate_endpoint(
    router: APIRouter,
    db_as_dependency: Session,
    restrict_endpoint_to_own_resources_param_user_id: Any,
):
    @router.get("/{user_id}/sessions/", response_model=list[UserSessionSchema], dependencies=[restrict_endpoint_to_own_resources_param_user_id])
    def get_user_quotes(
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        db: Session = db_as_dependency
    ):
        userSessions = crud_base.get_resource_items_by_attribute(db, UserSessionModel, UserSessionModel.user_id, user_id, skip=skip, limit=limit)
        return userSessions
