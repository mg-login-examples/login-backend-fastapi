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
    @router.get("/", response_model=list[User], dependencies=[current_user_dependency])
    def get_users(
        filter_users_text: str,
        skip: int = 0,
        limit: int = 100,
        db: Session = db_as_dependency
    ):
        if len(filter_users_text) < 3:
            return []
        sql_like_users = f'%{filter_users_text}%@%'
        users = crud_base.get_resource_items_by_attribute_filtered(db, UserModel, UserModel.email, sql_like_users, skip=skip, limit=limit)
        return users
