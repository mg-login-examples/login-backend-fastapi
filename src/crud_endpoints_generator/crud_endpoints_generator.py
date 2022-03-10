from typing import Callable

from fastapi import APIRouter

from .endpoints import get_items_count, get_items, get_item, post_item, put_item, delete_item
from .endpoints_required import Endpoints
from .resource_configurations import ResourceConfigurations


def get_resource_endpoints_router(
    endpoints_required: Endpoints,
    resource_configs: ResourceConfigurations,
    get_db_session: Callable
):
    router = APIRouter(prefix=f"/{resource_configs.resource_endpoints_url_prefix}")
    # GET count
    if endpoints_required.get_items_count:
        get_items_count.generate_endpoint(
            router,
            resource_configs.ResourceModel,
            get_db_session
        )
    # GET items
    if endpoints_required.get_items:
        get_items.generate_endpoint(
            router,
            resource_configs.ResourceModel,
            resource_configs.ResourceSchema,
            get_db_session
        )
    # GET item
    if endpoints_required.get_item:
        get_item.generate_endpoint(
            router,
            resource_configs.ResourceModel,
            resource_configs.ResourceSchema,
            get_db_session
        )
    # POST item
    if endpoints_required.post_item:
        post_item.generate_endpoint(
            router,
            resource_configs.ResourceModel,
            resource_configs.ResourceSchema,
            resource_configs.ResourceCreateSchema,
            resource_configs.customEndUserCreateSchemaToDbSchema,
            get_db_session
        )
    # PUT item
    if endpoints_required.put_item:
        put_item.generate_endpoint(
            router,
            resource_configs.ResourceModel,
            resource_configs.ResourceSchema,
            resource_configs.customEndUserUpdateSchemaToDbSchema,
            get_db_session
        )
    # DELETE item
    if endpoints_required.delete_item:
        delete_item.generate_endpoint(
            router,
            resource_configs.ResourceModel,
            get_db_session
        )

    return router
