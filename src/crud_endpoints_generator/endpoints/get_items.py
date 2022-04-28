from typing import List, Any

from fastapi import APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel as BaseSchema

from ..sqlalchemy_base_model import Base as BaseORMModel
from .. import crud_base

def generate_endpoint(
    router: APIRouter,
    dependencies: List[Any],
    db_as_dependency: Session,
    ResourceModel: BaseORMModel,
    ResourceSchema: BaseSchema
):
    @router.get("/", response_model=List[ResourceSchema], dependencies=dependencies)
    def get_items(skip: int = 0, limit: int = 100, db: Session = db_as_dependency) -> List[ResourceSchema]:
        return crud_base.get_resource_items(db, ResourceModel, skip=skip, limit=limit)
