from fastapi import APIRouter

from admin.api.resources import resourcesConfigurations
from api_dependencies.helper_classes.dependencies import Dependencies

from crud_endpoints_generator.crud_endpoints_generator import generate_router_with_resource_endpoints
from crud_endpoints_generator.endpoints_required import Endpoints
from admin.api.add_resource_url_ids_to_schema_properties import add_resource_url_ids_to_schema_properties

def add_all_admin_resources_routes(parent_router: APIRouter, dependencies: Dependencies) -> APIRouter:
    admin_router = APIRouter(prefix="/admin")

    _create_get_admin_resources_endpoints(admin_router)
    _create_crud_endpoints_for_all_admin_resources(admin_router, dependencies)

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

def _create_crud_endpoints_for_all_admin_resources(router: APIRouter, route_dependencies: Dependencies):
    endpoints_required = Endpoints().require_all()
    for resourceConfiguration in resourcesConfigurations:
        router.include_router(
            generate_router_with_resource_endpoints(
                endpoints_required,
                resourceConfiguration,
                route_dependencies
            ),
            prefix="/resource"
        )
