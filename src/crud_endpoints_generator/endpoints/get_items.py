from typing import Any

from sqlalchemy.orm import Session
from pydantic import BaseModel as BaseSchema
from pymongo.database import Database

from helpers_classes.custom_api_router import APIRouter
from stores.sql_db_store.sqlalchemy_base_model import Base as BaseORMModel
from stores.sql_db_store import crud_base as sql_crud_base
from stores.nosql_db_store import crud_base as mongo_crud_base

def generate_sql_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    db_as_dependency: Session,
    ResourceModel: BaseORMModel,
    ResourceSchema: BaseSchema
):
    @router.get("/", response_model=list[ResourceSchema], dependencies=dependencies)
    def get_items(skip: int = 0, limit: int = 100, db: Session = db_as_dependency) -> list[ResourceSchema]:
        return sql_crud_base.get_resource_items(db, ResourceModel, skip=skip, limit=limit)

def generate_mongo_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    db_as_dependency: Database,
    db_table: str,
    ResourceSchema: BaseSchema
):
    @router.get('/', response_model=list[ResourceSchema], response_model_by_alias=False, dependencies=dependencies)
    async def get_items(
        skip: int = 0,
        limit: int = 100,
        db: Database = db_as_dependency
    ):
        return mongo_crud_base.get_resource_items(
            db,
            db_table,
            ItemSchema=ResourceSchema,
            limit=limit,
            skip=skip
        )
