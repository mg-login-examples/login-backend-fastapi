from api_dependencies.admin_route_dependencies import AdminRouteDependencies
from crud_endpoints_generator.crud_endpoints_generator import \
    generate_router_with_resource_endpoints
from crud_endpoints_generator.endpoints_configs import EndpointsConfigs
from helpers_classes.custom_api_router import APIRouter
from rest_endpoints.admin.resources import resources_configurations


def generate_endpoints(
    router: APIRouter, admin_route_dependencies: AdminRouteDependencies
):
    for resource_configuration in resources_configurations:
        endpoints_required = EndpointsConfigs().require_all()
        if resource_configuration.MongoDBTable:
            endpoints_required.resource_in_mongo_db()
        router.include_router(
            generate_router_with_resource_endpoints(
                endpoints_required,
                resource_configuration,
                admin_route_dependencies.sql_db_session,
                admin_route_dependencies.mongo_db,
                route_dependencies=[admin_route_dependencies.validated_access_token],
            ),
            prefix="/resource",
        )
