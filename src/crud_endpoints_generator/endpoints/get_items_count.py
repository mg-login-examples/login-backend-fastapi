from typing import Callable

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..sqlalchemy_base_model import Base as BaseORMModel
from .. import crud_base

def generate_endpoint(
    router: APIRouter,
    ResourceModel: BaseORMModel,
    get_db_session: Callable
):
    @router.get("/count/", response_model=int)
    def get_resource_items_count(db: Session = Depends(get_db_session)) -> int:
        totalItemsCount = crud_base.get_resource_items_count(db, ResourceModel)
        return totalItemsCount
