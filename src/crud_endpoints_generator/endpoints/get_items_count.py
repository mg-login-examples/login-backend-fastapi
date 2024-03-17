from typing import Any

from helpers_classes.custom_api_router import APIRouter
from sqlalchemy.orm import Session
from pymongo.database import Database

from stores.sql_db_store.sqlalchemy_base_model import Base as BaseORMModel
from stores.sql_db_store import crud_base as sql_crud_base
from stores.nosql_db_store import crud_base as mongo_crud_base

def generate_sql_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    db_as_dependency: Session,
    ResourceModel: BaseORMModel,
):
    @router.get("/count/", response_model=int, dependencies=dependencies)
    def get_resource_items_count(db: Session = db_as_dependency) -> int:
        totalItemsCount = sql_crud_base.get_resource_items_count(db, ResourceModel)
        return totalItemsCount

def generate_mongo_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    db_as_dependency: Database,
    db_table: str,
):
    @router.get("/count/", response_model=int, dependencies=dependencies)
    def get_resource_items_count(db: Database = db_as_dependency) -> int:
        total_items_count = mongo_crud_base.get_resource_items_count(db, db_table)
        return total_items_count
