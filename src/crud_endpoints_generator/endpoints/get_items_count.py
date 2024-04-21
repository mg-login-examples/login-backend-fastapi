from typing import Any, Type

from fastapi import Request
from pydantic import BaseModel as BaseSchema
from pymongo.database import Database
from sqlalchemy.ext.declarative import DeclarativeMeta
from sqlalchemy.orm import Session

from helpers_classes.custom_api_router import APIRouter
from stores.nosql_db_store import crud_base as mongo_crud_base
from stores.sql_db_store import crud_base as sql_crud_base


def generate_sql_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    sql_db_session_as_dependency: Session,
    ResourceModel: Type[DeclarativeMeta],
    ResourceSchema: Type[BaseSchema],
):
    properties = ResourceSchema.model_json_schema()["properties"]
    filterable_fields = []
    for key in properties.keys():
        if "type" in properties[key] and properties[key]["type"] in [
            "string",
            "boolean",
            "integer",
            "float",
        ]:
            filterable_fields.append(key)

    @router.get("/count/", response_model=int, dependencies=dependencies)
    def get_resource_items_count(
        request: Request, sql_db_session: Session = sql_db_session_as_dependency
    ) -> int:
        ResourceModel_attributes = []
        attribute_filters = []
        for query_param_key in request.query_params.keys():
            if "_substring" in query_param_key:
                attribute = query_param_key.split("_substring")[0]
                if attribute in filterable_fields:
                    filter_value = request.query_params[query_param_key]
                    attribute_filter = f"%{filter_value}%"
                    ResourceModel_attributes.append(getattr(ResourceModel, attribute))
                    attribute_filters.append(attribute_filter)
        return (
            sql_crud_base.get_resource_items_filtered_by_like_multiple_attributes_count(
                sql_db_session,
                ResourceModel,
                ResourceModel_attributes,
                attribute_filters,
            )
        )


def generate_mongo_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    mongo_db_as_dependency: Database,
    db_table: str,
    ResourceSchema: Type[BaseSchema],
):
    @router.get("/count/", response_model=int, dependencies=dependencies)
    def get_resource_items_count(mongo_db: Database = mongo_db_as_dependency) -> int:
        total_items_count = mongo_crud_base.get_resource_items_count(mongo_db, db_table)
        return total_items_count
