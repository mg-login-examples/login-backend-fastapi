from api_dependencies.helper_classes.custom_api_router import APIRouter

from api_dependencies.helper_classes.dependencies import Dependencies

from .login_endpoint import generate_endpoint as generate_login_endpoint
from .authenticate_endpoint import generate_endpoint as generate_authentication_endpoint
from .logout_endpoint import generate_endpoint as generate_logout_endpoint
from .password_reset_link_endpoint import generate_endpoint as generate_password_reset_link_endpoint
from .password_reset_endpoint import generate_endpoint as generate_password_reset_endpoint

def add_authentication_routes(
    parent_router: APIRouter,
    route_dependencies: Dependencies,
    samesite: str,
    secure_cookies: bool
) -> APIRouter:
    router = APIRouter()

    generate_login_endpoint(router, route_dependencies.db, route_dependencies.access_token_store, samesite, secure_cookies)
    generate_authentication_endpoint(router, route_dependencies.current_user)
    generate_logout_endpoint(router, route_dependencies.db, route_dependencies.access_token_store, route_dependencies.validated_access_token,)
    generate_password_reset_link_endpoint(router, route_dependencies.db)
    generate_password_reset_endpoint(router, route_dependencies.db)

    parent_router.include_router(router)
    return router
