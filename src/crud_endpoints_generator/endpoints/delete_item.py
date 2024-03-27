from typing import Any, Type

from fastapi import status, Response, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from pymongo.database import Database

from stores.sql_db_store import crud_base as sql_crud_base
from stores.nosql_db_store import crud_base as mongo_crud_base


def generate_sql_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    sql_db_session_as_dependency: Session,
    ResourceModel: Type[DeclarativeMeta],
):
    @router.delete("/{item_id}/", status_code=status.HTTP_204_NO_CONTENT,
                   dependencies=dependencies)
    def delete_item(item_id: int,
                    sql_db_session: Session = sql_db_session_as_dependency):
        sql_crud_base.delete_resource_item(
            sql_db_session, ResourceModel, item_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)


def generate_mongo_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    mongo_db_as_dependency: Database,
    db_table: str,
):
    @router.delete("/{item_id}/", status_code=status.HTTP_204_NO_CONTENT,
                   dependencies=dependencies)
    def delete_item(item_id: str, mongo_db: Database = mongo_db_as_dependency):
        mongo_crud_base.delete_resource_item_by_id(
            mongo_db,
            db_table,
            item_id
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
