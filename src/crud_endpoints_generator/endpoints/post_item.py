from typing import List, Any, Callable

from sqlalchemy.orm import Session
from pydantic import BaseModel as BaseSchema

from helpers_classes.custom_api_router import APIRouter
from stores.sql_db_store.sqlalchemy_base_model import Base as BaseORMModel
from stores.sql_db_store import crud_base

def generate_endpoint(
    router: APIRouter,
    dependencies: List[Any],
    db_as_dependency: Session,
    ResourceModel: BaseORMModel,
    ResourceSchema: BaseSchema,
    ResourceCreateSchema: BaseSchema,
    customEndUserCreateSchemaToDbSchema: Callable,
):
    @router.post("/", response_model=ResourceSchema, dependencies=dependencies)
    def create_item(item: ResourceCreateSchema, db: Session = db_as_dependency) -> ResourceSchema:
        if customEndUserCreateSchemaToDbSchema:
            item = customEndUserCreateSchemaToDbSchema(item)
        return crud_base.create_resource_item(db, ResourceModel, item)
