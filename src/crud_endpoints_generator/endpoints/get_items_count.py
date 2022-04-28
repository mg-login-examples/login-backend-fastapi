from fastapi import APIRouter
from sqlalchemy.orm import Session

from ..sqlalchemy_base_model import Base as BaseORMModel
from .. import crud_base
from data.schemas.users.user import User

def generate_endpoint(
    router: APIRouter,
    current_user_as_dependency: User,
    db_as_dependency: Session,
    ResourceModel: BaseORMModel
):
    @router.get("/count/", response_model=int)
    def get_resource_items_count(
        current_user: User = current_user_as_dependency,
        db: Session = db_as_dependency
    ) -> int:
        totalItemsCount = crud_base.get_resource_items_count(db, ResourceModel)
        return totalItemsCount
