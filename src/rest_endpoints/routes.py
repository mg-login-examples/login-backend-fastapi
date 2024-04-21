import logging

from api_dependencies.admin_route_dependencies import AdminRouteDependencies
from api_dependencies.user_route_dependencies import UserRouteDependencies
from helpers_classes.custom_api_router import APIRouter
from rest_endpoints import health_check
from rest_endpoints.admin import routes as admin_routes
from rest_endpoints.user import routes as user_routes

logger = logging.getLogger(__name__)


def get_router(
    user_route_dependencies: UserRouteDependencies,
    admin_routes_dependencies: AdminRouteDependencies,
    user_auth_cookie_type: str,
    admin_user_auth_cookie_type: str,
    add_admin_app: bool,
) -> APIRouter:
    api_router = APIRouter(prefix="/api")
    health_check.generate_endpoint(api_router)

    if add_admin_app:
        admin_router = admin_routes.get_router(
            admin_routes_dependencies, admin_user_auth_cookie_type
        )
        api_router.include_router(admin_router)

    user_router = user_routes.get_router(user_route_dependencies, user_auth_cookie_type)
    api_router.include_router(user_router)

    return api_router
