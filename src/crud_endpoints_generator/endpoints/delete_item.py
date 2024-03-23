from typing import Any

from fastapi import status, Response, APIRouter
from sqlalchemy.orm import Session
from pymongo.database import Database

from stores.sql_db_store.sqlalchemy_base_model import Base as BaseORMModel
from stores.sql_db_store import crud_base as sql_crud_base
from stores.nosql_db_store import crud_base as mongo_crud_base

def generate_sql_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    db_as_dependency: Session,
    ResourceModel: BaseORMModel
):
    @router.delete("/{item_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=dependencies)
    def delete_item(item_id: int, db: Session = db_as_dependency):
        sql_crud_base.delete_resource_item(db, ResourceModel, item_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

def generate_mongo_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    db_as_dependency: Database,
    db_table: str,
):
    @router.delete("/{item_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=dependencies)
    def delete_item(item_id: str, db: Database = db_as_dependency):
        mongo_crud_base.delete_resource_item_by_id(
            db,
            db_table,
            item_id
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
