from typing import List, Any, Callable

from fastapi import status, HTTPException, APIRouter, Response
from sqlalchemy.orm import Session
from pymongo.database import Database
from pydantic import BaseModel as BaseSchema

from stores.sql_db_store.sqlalchemy_base_model import Base as BaseORMModel
from stores.sql_db_store import crud_base as sql_crud_base
from stores.nosql_db_store import crud_base as mongo_crud_base

def generate_sql_endpoint(
    router: APIRouter,
    dependencies: List[Any],
    db_as_dependency: Session,
    ResourceModel: BaseORMModel,
    ResourceSchema: BaseSchema,
    customEndUserUpdateSchemaToDbSchema: Callable,
):
    @router.put("/{item_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=dependencies)
    def update_item(item_id: int, item: ResourceSchema, db: Session = db_as_dependency) -> ResourceSchema:
        if item_id != item.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item id in request body different from path parameter")
        if customEndUserUpdateSchemaToDbSchema:
            item = customEndUserUpdateSchemaToDbSchema(item)
        db_item = sql_crud_base.update_resource_item_full(db, ResourceModel, item)
        if not db_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)

def generate_mongo_endpoint(
    router: APIRouter,
    dependencies: List[Any],
    db_as_dependency: Database,
    db_table: str,
    ResourceSchema: BaseSchema,
    customEndUserUpdateSchemaToDbSchema: Callable,
):
    @router.put("/{item_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=dependencies)
    def update_item(item_id: str, item: ResourceSchema, db: Database = db_as_dependency) -> ResourceSchema:
        if item_id != str(item.id):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item id in request body different from path parameter")
        if customEndUserUpdateSchemaToDbSchema:
            item = customEndUserUpdateSchemaToDbSchema(item)
        mongo_crud_base.update_item_by_id(
            db,
            db_table,
            item_id,
            item,
        )
        # if not db_item:
        #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)
