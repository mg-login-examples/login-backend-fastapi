from typing import List, Any

from sqlalchemy.orm import Session

from helpers_classes.custom_api_router import APIRouter
from stores.sql_db_store import crud_base
from data.database.models.user import User as UserModel
from data.schemas.users.user import User

def generate_endpoint(
    router: APIRouter,
    db_as_dependency: Session,
    current_user_dependency: User
):
    @router.post("/ids", response_model=List[User], dependencies=[current_user_dependency])
    def get_users_by_ids(
        user_ids: List[int],
        skip: int = 0,
        limit: int = 100,
        db: Session = db_as_dependency
    ):
        users = crud_base.get_resource_items_by_attribute_in_list(db, UserModel, UserModel.id, user_ids, skip=skip, limit=limit)
        return users
