from helpers_classes.custom_api_router import APIRouter
from rest_endpoints.admin import routes as admin_routes
from rest_endpoints.user import routes as user_routes
from api_dependencies.common_route_dependencies import CommonRouteDependencies

def get_router(
    api_routes_dependencies: CommonRouteDependencies,
    admin_routes_dependencies: CommonRouteDependencies,
    user_auth_cookie_type: str,
    admin_user_auth_cookie_type: str,
    add_admin_app: bool,
) -> APIRouter:
    api_router = APIRouter(prefix="/api")

    if add_admin_app:
        admin_router = admin_routes.get_router(admin_routes_dependencies, admin_user_auth_cookie_type)
        api_router.include_router(admin_router)

    user_router = user_routes.get_router(api_routes_dependencies, user_auth_cookie_type)
    api_router.include_router(user_router)

    return api_router    
