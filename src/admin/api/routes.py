from fastapi import APIRouter

from admin.api.resources import resourcesConfigurations

from crud_endpoints_generator.crud_endpoints_generator import get_resource_endpoints_router
from crud_endpoints_generator.endpoints_required import Endpoints
from admin.api.add_resource_url_ids_to_schema_properties import add_resource_url_ids_to_schema_properties
from app_configurations import app_db_manager

router = APIRouter(prefix="/admin")

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

endpoints_required = Endpoints().require_all()
for resourceConfiguration in resourcesConfigurations:
    router.include_router(
        get_resource_endpoints_router(
            endpoints_required,
            resourceConfiguration,
            app_db_manager.db_session
        ),
        prefix="/resource"
    )
