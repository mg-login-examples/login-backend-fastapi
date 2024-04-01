from typing import Any, Type

from fastapi import status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from pymongo.database import Database
from pydantic import BaseModel as BaseSchema

from stores.sql_db_store import crud_base as sql_crud_base
from stores.nosql_db_store import crud_base as mongo_crud_base


def generate_sql_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    sql_db_session_as_dependency: Session,
    ResourceModel: Type[DeclarativeMeta],
    ResourceSchema: Type[BaseSchema],
):
    @router.get("/{item_id}/", response_model=ResourceSchema, dependencies=dependencies)
    def get_resource_item(
        item_id: int, sql_db_session: Session = sql_db_session_as_dependency
    ):
        item = sql_crud_base.get_resource_item(sql_db_session, ResourceModel, item_id)
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )
        return item


def generate_mongo_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    mongo_db_as_dependency: Database,
    db_table: str,
    ResourceSchema: Type[BaseSchema],
):
    @router.get(
        "/{item_id}/",
        response_model=ResourceSchema,
        response_model_by_alias=False,
        dependencies=dependencies,
    )
    def get_resource_item(item_id: str, mongo_db: Database = mongo_db_as_dependency):
        item = mongo_crud_base.get_resource_item_by_id(
            mongo_db,
            db_table,
            item_id,
        )
        if not item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )
        return item
