from typing import Callable, List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from pydantic import BaseModel as BaseSchema

from ..sqlalchemy_base_model import Base as BaseORMModel
from .. import crud_base


def generate_endpoint(
    router: APIRouter,
    ResourceModel: BaseORMModel,
    ResourceSchema: BaseSchema,
    get_db_session: Callable
):
    @router.get("/", response_model=List[ResourceSchema])
    def get_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db_session)) -> List[ResourceSchema]:
        return crud_base.get_resource_items(db, ResourceModel, skip=skip, limit=limit)
