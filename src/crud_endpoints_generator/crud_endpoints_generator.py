import logging
from typing import List, Any

from sqlalchemy.orm import Session

from helpers_classes.custom_api_router import APIRouter
from .endpoints import get_items_count, get_items, get_item, post_item, put_item, delete_item
from .endpoints_configs import EndpointsConfigs
from .resource_configurations import ResourceConfigurations

logger = logging.getLogger(__name__)

def generate_router_with_resource_endpoints(
    endpoints_configs: EndpointsConfigs,
    resource_configs: ResourceConfigurations,
    db_as_dependency: Session,
    route_dependencies: List[Any] = None,
):
    if route_dependencies is None:
        route_dependencies = []
    router = APIRouter(prefix=f"/{resource_configs.resource_endpoints_url_prefix}")
    # GET count
    if endpoints_configs.get_items_count.add:
        get_items_count.generate_endpoint(
            router,
            route_dependencies + endpoints_configs.get_items_count.dependencies,
            db_as_dependency,
            resource_configs.ResourceModel
        )
    # GET items
    if endpoints_configs.get_items.add:
        get_items.generate_endpoint(
            router,
            route_dependencies + endpoints_configs.get_items.dependencies,
            db_as_dependency,
            resource_configs.ResourceModel,
            resource_configs.ResourceSchema
        )
    # GET item
    if endpoints_configs.get_item.add:
        get_item.generate_endpoint(
            router,
            route_dependencies + endpoints_configs.get_item.dependencies,
            db_as_dependency,
            resource_configs.ResourceModel,
            resource_configs.ResourceSchema
        )
    # POST item
    if endpoints_configs.post_item.add:
        post_item.generate_endpoint(
            router,
            route_dependencies + endpoints_configs.post_item.dependencies,
            db_as_dependency,
            resource_configs.ResourceModel,
            resource_configs.ResourceSchema,
            resource_configs.ResourceCreateSchema,
            resource_configs.customEndUserCreateSchemaToDbSchema
        )
    # PUT item
    if endpoints_configs.put_item.add:
        put_item.generate_endpoint(
            router,
            route_dependencies + endpoints_configs.put_item.dependencies,
            db_as_dependency,
            resource_configs.ResourceModel,
            resource_configs.ResourceSchema,
            resource_configs.customEndUserUpdateSchemaToDbSchema,
        )
    # DELETE item
    if endpoints_configs.delete_item.add:
        delete_item.generate_endpoint(
            router,
            route_dependencies + endpoints_configs.delete_item.dependencies,
            db_as_dependency,
            resource_configs.ResourceModel
        )

    return router
