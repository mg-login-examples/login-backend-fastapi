from typing import List

from fastapi import APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel as BaseSchema

from ..sqlalchemy_base_model import Base as BaseORMModel
from .. import crud_base
from data.schemas.users.user import User

def generate_endpoint(
    router: APIRouter,
    current_user_as_dependency: User,
    db_as_dependency: Session,
    ResourceModel: BaseORMModel,
    ResourceSchema: BaseSchema
):
    @router.get("/", response_model=List[ResourceSchema])
    def get_items(
        skip: int = 0,
        limit: int = 100,
        current_user: User = current_user_as_dependency,
        db: Session = db_as_dependency
    ) -> List[ResourceSchema]:
        return crud_base.get_resource_items(db, ResourceModel, skip=skip, limit=limit)
