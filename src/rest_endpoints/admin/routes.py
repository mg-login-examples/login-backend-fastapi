from helpers_classes.custom_api_router import APIRouter
from api_dependencies.common_route_dependencies import CommonRouteDependencies
from rest_endpoints.admin.get_admin_resources_info_endpoint import generate_endpoint as generate_get_admin_resources_info_endpoint
from rest_endpoints.admin.admin_resources_crud_endpoints import generate_endpoints as generate_admin_resources_crud_endpoints
from rest_endpoints.admin.authentication import routes as authentication_routes

def get_router(
    dependencies: CommonRouteDependencies,
    auth_cookie_type: str
) -> APIRouter:
    router = APIRouter(prefix="/admin")

    generate_get_admin_resources_info_endpoint(router, dependencies)
    generate_admin_resources_crud_endpoints(router, dependencies)

    auth_router = authentication_routes.get_router(dependencies, auth_cookie_type)
    router.include_router(auth_router)

    return router
