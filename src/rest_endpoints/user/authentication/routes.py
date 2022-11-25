from helpers_classes.custom_api_router import APIRouter

from api_dependencies.common_route_dependencies import CommonRouteDependencies

from .login_endpoint import generate_endpoint as generate_login_endpoint
from .authenticate_endpoint import generate_endpoint as generate_authentication_endpoint
from .logout_endpoint import generate_endpoint as generate_logout_endpoint
from .password_reset_link_endpoint import generate_endpoint as generate_password_reset_link_endpoint
from .password_reset_endpoint import generate_endpoint as generate_password_reset_endpoint
from .password_change_endpoint import generate_endpoint as generate_password_change_endpoint

def get_router(
    route_dependencies: CommonRouteDependencies,
    auth_cookie_type: str,
) -> APIRouter:
    router = APIRouter()

    generate_login_endpoint(router, route_dependencies.db, route_dependencies.access_token_store, auth_cookie_type)
    generate_authentication_endpoint(router, route_dependencies.current_user)
    generate_logout_endpoint(router, route_dependencies.db, route_dependencies.access_token_store, route_dependencies.validated_access_token,)
    generate_password_reset_link_endpoint(router, route_dependencies.db)
    generate_password_reset_endpoint(router, route_dependencies.db)
    generate_password_change_endpoint(router, route_dependencies.db, route_dependencies.access_token_store, route_dependencies.current_user, auth_cookie_type)

    return router
