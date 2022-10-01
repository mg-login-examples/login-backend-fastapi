from helpers_classes.custom_api_router import APIRouter
from rest_endpoints.admin.resources import resources_configurations
from api_dependencies.common_route_dependencies import CommonRouteDependencies
from crud_endpoints_generator.crud_endpoints_generator import generate_router_with_resource_endpoints
from crud_endpoints_generator.endpoints_configs import EndpointsConfigs

def generate_endpoints(router: APIRouter, route_dependencies: CommonRouteDependencies):
    for resource_configuration in resources_configurations:
        endpoints_required = EndpointsConfigs().require_all()
        if resource_configuration.MongoDBTable:
            endpoints_required.resource_in_mongo_db()
        router.include_router(
            generate_router_with_resource_endpoints(
                endpoints_required,
                resource_configuration,
                route_dependencies.db,
                route_dependencies.nosql_database,
                route_dependencies=[route_dependencies.validated_access_token]
            ),
            prefix="/resource"
        )
