from typing import Any, Callable, Type

from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from pymongo.database import Database
from pydantic import BaseModel as BaseSchema

from helpers_classes.custom_api_router import APIRouter
from stores.sql_db_store import crud_base as sql_crud_base
from stores.nosql_db_store import crud_base as mongo_crud_base


def generate_sql_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    sql_db_session_as_dependency: Session,
    ResourceModel: Type[DeclarativeMeta],
    ResourceSchema: Type[BaseSchema],
    ResourceCreateSchema: Type[BaseSchema],
    customEndUserCreateSchemaToDbSchema: Callable | None,
):
    @router.post("/", response_model=ResourceSchema, dependencies=dependencies)
    def create_item(item: ResourceCreateSchema,  # type: ignore
                    sql_db_session: Session = sql_db_session_as_dependency):
        if customEndUserCreateSchemaToDbSchema:
            item = customEndUserCreateSchemaToDbSchema(item)
        return sql_crud_base.create_resource_item(
            sql_db_session, ResourceModel, item)


def generate_mongo_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    mongo_db_as_dependency: Database,
    db_table: str,
    ResourceSchema: Type[BaseSchema],
    ResourceCreateSchema: Type[BaseSchema],
    customEndUserCreateSchemaToDbSchema: Callable | None,

):
    @router.post("/", response_model=ResourceSchema,
                 response_model_by_alias=False, dependencies=dependencies)
    async def create_item(item: ResourceCreateSchema,  # type: ignore
                          mongo_db: Database = mongo_db_as_dependency):
        if customEndUserCreateSchemaToDbSchema:
            item = customEndUserCreateSchemaToDbSchema(item)
        return mongo_crud_base.create_resource_item(
            mongo_db,
            db_table,
            item,
        )
