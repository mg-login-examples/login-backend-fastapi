from typing import Callable

from api_dependencies.helper_classes.custom_api_router import APIRouter
from api.admin.example.resources import resourcesConfigurations
from crud_endpoints_generator.crud_endpoints_generator import get_resource_endpoints_router
from crud_endpoints_generator.endpoints_configs import EndpointsConfigs
from api.admin.add_resource_url_ids_to_schema_properties import add_resource_url_ids_to_schema_properties

def add_all_admin_resources_routes(parent_router: APIRouter, get_db_session: Callable) -> APIRouter:
    admin_router = APIRouter(prefix="/admin")

    _create_get_admin_resources_endpoints(admin_router)
    _create_crud_endpoints_for_all_admin_resources(admin_router, get_db_session)

    parent_router.include_router(admin_router)
    return parent_router


def _create_get_admin_resources_endpoints(router: APIRouter):
    @router.get("/resources/")
    def get_all_resources():
        infos = []
        for resourceConfiguration in resourcesConfigurations:
            info = {
                "resourceUrlId": resourceConfiguration.resource_endpoints_url_prefix,
                "resourceName": resourceConfiguration.ResourceSchema.schema()["title"],
                "updateSchema": resourceConfiguration.ResourceSchema.schema(),
                "createSchema": resourceConfiguration.ResourceCreateSchema.schema(),
            }
            add_resource_url_ids_to_schema_properties(info["updateSchema"], resourceConfiguration, resourcesConfigurations)
            add_resource_url_ids_to_schema_properties(info["createSchema"], resourceConfiguration, resourcesConfigurations)
            infos.append(info)
        return infos


def _create_crud_endpoints_for_all_admin_resources(router: APIRouter, get_db_session: Callable):
    endpoints_required = EndpointsConfigs().require_all()
    for resourceConfiguration in resourcesConfigurations:
        router.include_router(
            get_resource_endpoints_router(
                endpoints_required,
                resourceConfiguration,
                get_db_session
            ),
            prefix="/resource"
        )
