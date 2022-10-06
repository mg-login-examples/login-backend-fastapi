from typing import List, Any, Callable

from sqlalchemy.orm import Session
from pymongo.database import Database
from pydantic import BaseModel as BaseSchema

from helpers_classes.custom_api_router import APIRouter
from stores.sql_db_store.sqlalchemy_base_model import Base as BaseORMModel
from stores.sql_db_store import crud_base as sql_crud_base
from stores.nosql_db_store import crud_base as mongo_crud_base

def generate_sql_endpoint(
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
        return sql_crud_base.create_resource_item(db, ResourceModel, item)

def generate_mongo_endpoint(
    router: APIRouter,
    dependencies: List[Any],
    db_as_dependency: Database,
    db_table: str,
    ResourceSchema: BaseSchema,
    ResourceCreateSchema: BaseSchema,
    customEndUserCreateSchemaToDbSchema: Callable,
    
):
    @router.post("/", response_model=ResourceSchema, response_model_by_alias=False, dependencies=dependencies)
    async def create_item(item: ResourceCreateSchema, db: Database = db_as_dependency):
        if customEndUserCreateSchemaToDbSchema:
            item = customEndUserCreateSchemaToDbSchema(item)
        return mongo_crud_base.create_resource_item(
            db,
            db_table,
            item,
            ItemSchema=ResourceSchema
        )
