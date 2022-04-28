from typing import Callable

from fastapi import APIRouter

from api_dependencies.helper_classes.dependencies import Dependencies

from .endpoints import get_items_count, get_items, get_item, post_item, put_item, delete_item
from .endpoints_required import Endpoints
from .resource_configurations import ResourceConfigurations


def generate_router_with_resource_endpoints(
    endpoints_required: Endpoints,
    resource_configs: ResourceConfigurations,
    route_dependencies: Dependencies,
):
    router = APIRouter(prefix=f"/{resource_configs.resource_endpoints_url_prefix}")
    # GET count
    if endpoints_required.get_items_count:
        get_items_count.generate_endpoint(
            router,
            route_dependencies.current_user,
            route_dependencies.db,
            resource_configs.ResourceModel
        )
    # GET items
    if endpoints_required.get_items:
        get_items.generate_endpoint(
            router,
            route_dependencies.current_user,
            route_dependencies.db,
            resource_configs.ResourceModel,
            resource_configs.ResourceSchema
        )
    # GET item
    if endpoints_required.get_item:
        get_item.generate_endpoint(
            router,
            route_dependencies.current_user,
            route_dependencies.db,
            resource_configs.ResourceModel,
            resource_configs.ResourceSchema
        )
    # POST item
    if endpoints_required.post_item:
        post_item.generate_endpoint(
            router,
            route_dependencies.current_user,
            route_dependencies.db,
            resource_configs.ResourceModel,
            resource_configs.ResourceSchema,
            resource_configs.ResourceCreateSchema,
            resource_configs.customEndUserCreateSchemaToDbSchema
        )
    # PUT item
    if endpoints_required.put_item:
        put_item.generate_endpoint(
            router,
            route_dependencies.current_user,
            route_dependencies.db,
            resource_configs.ResourceModel,
            resource_configs.ResourceSchema,
            resource_configs.customEndUserUpdateSchemaToDbSchema,
        )
    # DELETE item
    if endpoints_required.delete_item:
        delete_item.generate_endpoint(
            router,
            route_dependencies.current_user,
            route_dependencies.db,
            resource_configs.ResourceModel
        )

    return router
