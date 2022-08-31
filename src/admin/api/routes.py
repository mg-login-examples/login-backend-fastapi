from api_dependencies.helper_classes.custom_api_router import APIRouter
from admin.api.resources import resourcesConfigurations
from api_dependencies.helper_classes.dependencies import Dependencies

from crud_endpoints_generator.crud_endpoints_generator import generate_router_with_resource_endpoints
from crud_endpoints_generator.endpoints_configs import EndpointsConfigs
from admin.api.add_resource_url_ids_to_schema_properties import add_resource_url_ids_to_schema_properties
from admin.api.authentication.routes import add_authentication_routes

def add_all_admin_resources_routes(
    parent_router: APIRouter,
    dependencies: Dependencies,
    secure_cookies: bool
) -> APIRouter:
    admin_router = APIRouter(prefix="/admin")

    _create_get_admin_resources_endpoints(admin_router, dependencies)
    _create_crud_endpoints_for_all_admin_resources(admin_router, dependencies)
    add_authentication_routes(admin_router, dependencies, secure_cookies)

    parent_router.include_router(admin_router)
    return parent_router


def _create_get_admin_resources_endpoints(router: APIRouter, route_dependencies: Dependencies):
    @router.get("/resources/", dependencies=[route_dependencies.validated_access_token])
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
    endpoints_required = EndpointsConfigs().require_all()
    for resourceConfiguration in resourcesConfigurations:
        router.include_router(
            generate_router_with_resource_endpoints(
                endpoints_required,
                resourceConfiguration,
                route_dependencies.db,
                route_dependencies=[route_dependencies.validated_access_token]
            ),
            prefix="/resource"
        )
