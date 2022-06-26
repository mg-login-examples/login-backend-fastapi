from typing import List, Any

from api_dependencies.helper_classes.custom_api_router import APIRouter
from sqlalchemy.orm import Session

from ..sqlalchemy_base_model import Base as BaseORMModel
from .. import crud_base

def generate_endpoint(
    router: APIRouter,
    dependencies: List[Any],
    db_as_dependency: Session,
    ResourceModel: BaseORMModel
):
    @router.get("/count/", response_model=int, dependencies=dependencies)
    def get_resource_items_count(db: Session = db_as_dependency) -> int:
        totalItemsCount = crud_base.get_resource_items_count(db, ResourceModel)
        return totalItemsCount
