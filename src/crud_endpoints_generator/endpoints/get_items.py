from typing import Any, Type

from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import DeclarativeMeta
from pydantic import BaseModel as BaseSchema
from pymongo.database import Database
from fastapi import Request

from helpers_classes.custom_api_router import APIRouter
from stores.sql_db_store import crud_base as sql_crud_base
from stores.nosql_db_store import crud_base as mongo_crud_base


def generate_sql_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    sql_db_session_as_dependency: Session,
    ResourceModel: Type[DeclarativeMeta],
    ResourceSchema: Type[BaseSchema]
):
    properties = ResourceSchema.model_json_schema()['properties']
    filterable_fields = []
    for key in properties.keys():
        if 'type' in properties[key] and properties[key]['type'] in [
                'string', 'boolean', 'integer', 'float']:
            filterable_fields.append(key)

    @router.get("/",
                response_model=list[ResourceSchema],  # type: ignore
                dependencies=dependencies)
    def get_items(request: Request, skip: int = 0, limit: int = 100,
                  sql_db_session: Session = sql_db_session_as_dependency):
        ResourceModel_attributes = []
        attribute_filters = []
        for query_param_key in request.query_params.keys():
            if "_substring" in query_param_key:
                attribute = query_param_key.split("_substring")[0]
                if attribute in filterable_fields:
                    filter_value = request.query_params[query_param_key]
                    attribute_filter = f'%{filter_value}%'
                    ResourceModel_attributes.append(
                        getattr(ResourceModel, attribute))
                    attribute_filters.append(attribute_filter)
        return sql_crud_base.get_resource_items_filtered_by_like_multiple_attributes(
            sql_db_session, ResourceModel, ResourceModel_attributes, attribute_filters, skip=skip, limit=limit)


def generate_mongo_endpoint(
    router: APIRouter,
    dependencies: list[Any],
    mongo_db_as_dependency: Database,
    db_table: str,
    ResourceSchema: Type[BaseSchema]
):
    @router.get('/', response_model=list[ResourceSchema],  # type: ignore
                response_model_by_alias=False, dependencies=dependencies)
    async def get_items(
        skip: int = 0,
        limit: int = 100,
        mongo_db: Database = mongo_db_as_dependency
    ):
        return mongo_crud_base.get_resource_items_pydantized(
            mongo_db,
            db_table,
            ResourceSchema,
            limit=limit,
            skip=skip
        )
