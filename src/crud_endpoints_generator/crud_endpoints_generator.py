import logging
from typing import Any

from sqlalchemy.orm import Session
from pymongo.database import Database

from helpers_classes.custom_api_router import APIRouter
from .endpoints import get_items_count, get_items, get_item, post_item, put_item, delete_item
from .endpoints_configs import EndpointsConfigs
from .resource_configurations import ResourceConfigurations

logger = logging.getLogger(__name__)

def generate_router_with_resource_endpoints(
    endpoints_configs: EndpointsConfigs,
    resource_configs: ResourceConfigurations,
    sql_db_as_dependency: Session,
    mongo_db_as_dependency: Database,
    route_dependencies: list[Any] = None,
):
    if route_dependencies is None:
        route_dependencies = []
    router = APIRouter(prefix=f"/{resource_configs.resource_endpoints_url_prefix}")

    # GET count
    if endpoints_configs.get_items_count.add:
        if endpoints_configs.sql_db:
            get_items_count.generate_sql_endpoint(
                router,
                route_dependencies + endpoints_configs.get_items_count.dependencies,
                sql_db_as_dependency,
                resource_configs.ResourceModel
            )
        else:
            get_items_count.generate_mongo_endpoint(
                router,
                route_dependencies + endpoints_configs.get_items_count.dependencies,
                mongo_db_as_dependency,
                resource_configs.MongoDBTable
            )
    # GET items
    if endpoints_configs.get_items.add:
        if endpoints_configs.sql_db:
            get_items.generate_sql_endpoint(
                router,
                route_dependencies + endpoints_configs.get_items.dependencies,
                sql_db_as_dependency,
                resource_configs.ResourceModel,
                resource_configs.ResourceSchema
            )
        else:
            get_items.generate_mongo_endpoint(
                router,
                route_dependencies + endpoints_configs.get_items.dependencies,
                mongo_db_as_dependency,
                resource_configs.MongoDBTable,
                resource_configs.ResourceSchema
            )
    # GET item
    if endpoints_configs.get_item.add:
        if endpoints_configs.sql_db:
            get_item.generate_sql_endpoint(
                router,
                route_dependencies + endpoints_configs.get_item.dependencies,
                sql_db_as_dependency,
                resource_configs.ResourceModel,
                resource_configs.ResourceSchema
            )
        else:
            get_item.generate_mongo_endpoint(
                router,
                route_dependencies + endpoints_configs.get_item.dependencies,
                mongo_db_as_dependency,
                resource_configs.MongoDBTable,
                resource_configs.ResourceSchema
            )
    # POST item
    if endpoints_configs.post_item.add:
        if endpoints_configs.sql_db:
            post_item.generate_sql_endpoint(
                router,
                route_dependencies + endpoints_configs.post_item.dependencies,
                sql_db_as_dependency,
                resource_configs.ResourceModel,
                resource_configs.ResourceSchema,
                resource_configs.ResourceCreateSchema,
                resource_configs.customEndUserCreateSchemaToDbSchema
            )
        else:
            post_item.generate_mongo_endpoint(
                router,
                route_dependencies + endpoints_configs.post_item.dependencies,
                mongo_db_as_dependency,
                resource_configs.MongoDBTable,
                resource_configs.ResourceSchema,
                resource_configs.ResourceCreateSchema,
                resource_configs.customEndUserCreateSchemaToDbSchema
            )
    # PUT item
    if endpoints_configs.put_item.add:
        if endpoints_configs.sql_db:
            put_item.generate_sql_endpoint(
                router,
                route_dependencies + endpoints_configs.put_item.dependencies,
                sql_db_as_dependency,
                resource_configs.ResourceModel,
                resource_configs.ResourceSchema,
                resource_configs.customEndUserUpdateSchemaToDbSchema,
            )
        else:
            put_item.generate_mongo_endpoint(
                router,
                route_dependencies + endpoints_configs.put_item.dependencies,
                mongo_db_as_dependency,
                resource_configs.MongoDBTable,
                resource_configs.ResourceSchema,
                resource_configs.customEndUserUpdateSchemaToDbSchema,
            )
    # DELETE item
    if endpoints_configs.delete_item.add:
        if endpoints_configs.sql_db:
            delete_item.generate_sql_endpoint(
                router,
                route_dependencies + endpoints_configs.delete_item.dependencies,
                sql_db_as_dependency,
                resource_configs.ResourceModel
            )
        else:
            delete_item.generate_mongo_endpoint(
                router,
                route_dependencies + endpoints_configs.delete_item.dependencies,
                mongo_db_as_dependency,
                resource_configs.MongoDBTable
            )

    return router
