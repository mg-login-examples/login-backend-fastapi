from helpers_classes.custom_api_router import APIRouter
from api_dependencies.admin_route_dependencies import AdminRouteDependencies

from .login_endpoint import generate_endpoint as generate_login_endpoint
from .authenticate_endpoint import generate_endpoint as generate_authentication_endpoint
from .logout_endpoint import generate_endpoint as generate_logout_endpoint


def get_router(
    admin_route_dependencies: AdminRouteDependencies,
    auth_cookie_type: str
) -> APIRouter:
    router = APIRouter()

    generate_login_endpoint(router, admin_route_dependencies.sql_db_session,
                            admin_route_dependencies.access_token_store, auth_cookie_type)
    generate_authentication_endpoint(
        router, admin_route_dependencies.current_admin_user)
    generate_logout_endpoint(router, admin_route_dependencies.validated_access_token,
                             admin_route_dependencies.access_token_store)

    return router
