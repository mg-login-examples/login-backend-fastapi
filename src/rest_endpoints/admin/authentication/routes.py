from helpers_classes.custom_api_router import APIRouter
from api_dependencies.common_route_dependencies import CommonRouteDependencies

from .login_endpoint import generate_endpoint as generate_login_endpoint
from .authenticate_endpoint import generate_endpoint as generate_authentication_endpoint
from .logout_endpoint import generate_endpoint as generate_logout_endpoint

def get_router(
    route_dependencies: CommonRouteDependencies,
    auth_cookie_type: str
) -> APIRouter:
    router = APIRouter()

    generate_login_endpoint(router, route_dependencies.db, route_dependencies.access_token_store, auth_cookie_type)
    generate_authentication_endpoint(router, route_dependencies.current_user)
    generate_logout_endpoint(router, route_dependencies.validated_access_token, route_dependencies.access_token_store)

    return router
