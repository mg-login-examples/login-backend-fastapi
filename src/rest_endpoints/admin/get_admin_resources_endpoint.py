from helpers_classes.custom_api_router import APIRouter
from rest_endpoints.admin.resources import resources_configurations
from api_dependencies.common_route_dependencies import CommonRouteDependencies
from rest_endpoints.admin.add_resource_url_ids_to_schema_properties import add_resource_url_ids_to_schema_properties

def generate_endpoint(router: APIRouter, route_dependencies: CommonRouteDependencies):
    @router.get("/resources/", dependencies=[route_dependencies.validated_access_token])
    def get_all_resources():
        infos = []
        for resource_configuration in resources_configurations:
            info = {
                "resourceUrlId": resource_configuration.resource_endpoints_url_prefix,
                "resourceName": resource_configuration.ResourceSchema.schema()["title"],
                "updateSchema": resource_configuration.ResourceSchema.schema(by_alias=False),
                "createSchema": resource_configuration.ResourceCreateSchema.schema(by_alias=False),
            }
            add_resource_url_ids_to_schema_properties(info["updateSchema"], resources_configurations, resources_configurations)
            add_resource_url_ids_to_schema_properties(info["createSchema"], resources_configurations, resources_configurations)
            infos.append(info)
        return infos
