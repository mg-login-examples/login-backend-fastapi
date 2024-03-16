from helpers_classes.custom_api_router import APIRouter
from rest_endpoints.admin.resources import resources_configurations
from api_dependencies.common_route_dependencies import CommonRouteDependencies
from rest_endpoints.admin.enhance_resource_schemas import enhance_resource_schemas

def generate_endpoint(router: APIRouter, route_dependencies: CommonRouteDependencies):
    @router.get("/resources/", dependencies=[route_dependencies.validated_access_token])
    def get_all_resources():
        infos = []
        for resource_configuration in resources_configurations:
            info = {
                "resourceUrlId": resource_configuration.resource_endpoints_url_prefix,
                "resourceName": resource_configuration.ResourceSchema.model_json_schema()["title"],
                "createSchema": resource_configuration.ResourceCreateSchema.model_json_schema(by_alias=False),
                "updateSchema": resource_configuration.ResourceSchema.model_json_schema(by_alias=False),
            }
            enhance_resource_schemas(
                info["updateSchema"],
                info["createSchema"],
                resource_configuration,
                resources_configurations,
                resource_configuration.MongoDBTable == None,
            )
            infos.append(info)
        return infos
