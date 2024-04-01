from typing import Any

from sqlalchemy.orm import Session

from helpers_classes.custom_api_router import APIRouter
from stores.sql_db_store import crud_base
from data.database.models.user import User as UserModel
from data.schemas.users.user import User


def generate_endpoint(
    router: APIRouter,
    sql_db_session_as_dependency: Session,
    current_user_dependency: User,
):
    @router.post(
        "/ids", response_model=list[User], dependencies=[current_user_dependency]
    )  # type: ignore
    def get_users_by_ids(
        user_ids: list[int],
        skip: int = 0,
        limit: int = 100,
        sql_db_session: Session = sql_db_session_as_dependency,
    ):
        users = crud_base.get_resource_items_by_attribute_in_list(
            sql_db_session, UserModel, UserModel.id, user_ids, skip=skip, limit=limit
        )
        return users
