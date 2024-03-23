from typing import Any

from sqlalchemy.orm import Session
from pydantic import BaseModel as BaseSchema
from pymongo.database import Database
from fastapi import Request

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
    properties = ResourceSchema.schema()['properties']
    filterable_fields = []
    for key in properties.keys():
        if 'type' in properties[key] and properties[key]['type'] in ['string', 'boolean', 'integer', 'float']:
            filterable_fields.append(key)
    @router.get("/count/", response_model=int, dependencies=dependencies)
    def get_resource_items_count(request: Request, db: Session = db_as_dependency) -> int:
        ResourceModel_attributes = []
        attribute_filters = []
        for query_param_key in request.query_params.keys():
            if "_substring" in query_param_key:
                attribute = query_param_key.split("_substring")[0]
                if attribute in filterable_fields:
                    filter_value = request.query_params[query_param_key]
                    attribute_filter = f'%{filter_value}%'
                    ResourceModel_attributes.append(getattr(ResourceModel,attribute))
                    attribute_filters.append(attribute_filter)
        return sql_crud_base.get_resource_items_filtered_by_like_multiple_attributes_count(db, ResourceModel, ResourceModel_attributes, attribute_filters)
        # totalItemsCount = sql_crud_base.get_resource_items_count(db, ResourceModel)
        # return totalItemsCount

def generate_mongo_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    db_as_dependency: Database,
    db_table: str,
    ResourceSchema: BaseSchema
):
    @router.get("/count/", response_model=int, dependencies=dependencies)
    def get_resource_items_count(db: Database = db_as_dependency) -> int:
        total_items_count = mongo_crud_base.get_resource_items_count(db, db_table)
        return total_items_count
