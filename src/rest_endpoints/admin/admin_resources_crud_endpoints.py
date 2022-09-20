from api_dependencies.helper_classes.custom_api_router import APIRouter
from rest_endpoints.admin.resources import resourcesConfigurations
from api_dependencies.helper_classes.dependencies import Dependencies
from crud_endpoints_generator.crud_endpoints_generator import generate_router_with_resource_endpoints
from crud_endpoints_generator.endpoints_configs import EndpointsConfigs

def generate_endpoints(router: APIRouter, route_dependencies: Dependencies):
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
