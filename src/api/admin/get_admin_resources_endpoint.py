from api_dependencies.helper_classes.custom_api_router import APIRouter
from api.admin.resources import resourcesConfigurations
from api_dependencies.helper_classes.dependencies import Dependencies
from api.admin.add_resource_url_ids_to_schema_properties import add_resource_url_ids_to_schema_properties

def generate_endpoint(router: APIRouter, route_dependencies: Dependencies):
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
