from typing import Any, Callable, Type

from fastapi import status, HTTPException, APIRouter, Response
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
    customEndUserUpdateSchemaToDbSchema: Callable | None,
):
    @router.put(
        "/{item_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=dependencies
    )
    def update_item(
        item_id: int,
        item: ResourceSchema,  # type: ignore
        sql_db_session: Session = sql_db_session_as_dependency,
    ) -> Response:
        if not hasattr(item, "id"):
            raise Exception(f'ResourceSchema "{ResourceSchema}" has no id')
        if item_id != item.id:  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item id in request body different from path parameter",
            )
        if customEndUserUpdateSchemaToDbSchema:
            item = customEndUserUpdateSchemaToDbSchema(item)
        db_item = sql_crud_base.update_resource_item_full(
            sql_db_session, ResourceModel, item
        )
        if not db_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)


def generate_mongo_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    mongo_db_as_dependency: Database,
    db_table: str,
    ResourceSchema: Type[BaseSchema],
    customEndUserUpdateSchemaToDbSchema: Callable | None,
):
    @router.put(
        "/{item_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=dependencies
    )
    def update_item(
        item_id: str,
        item: ResourceSchema,  # type: ignore
        mongo_db: Database = mongo_db_as_dependency,
    ) -> Response:
        if not hasattr(item, "id"):
            raise Exception(f'ResourceSchema "{ResourceSchema}" has no id')
        if item_id != str(item.id):  # type: ignore
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Item id in request body different from path parameter",
            )
        if customEndUserUpdateSchemaToDbSchema:
            item = customEndUserUpdateSchemaToDbSchema(item)
        mongo_crud_base.update_item_by_id(
            mongo_db,
            db_table,
            item_id,
            item,
        )
        # if not db_item:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
