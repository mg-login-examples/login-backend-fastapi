from api_dependencies.helper_classes.custom_api_router import APIRouter

from api_dependencies.helper_classes.dependencies import Dependencies
from data.access_tokens_store.access_token_manager import AccessTokenManager

from .login_endpoint import generate_endpoint as generate_login_endpoint
from .authenticate_endpoint import generate_endpoint as generate_authentication_endpoint
from .logout_endpoint import generate_endpoint as generate_logout_endpoint
from .password_reset_link_endpoint import generate_endpoint as generate_password_reset_link_endpoint
from .password_reset_endpoint import generate_endpoint as generate_password_reset_endpoint

def add_authentication_routes(
    parent_router: APIRouter,
    route_dependencies: Dependencies,
    access_token_manager: AccessTokenManager,
    samesite: str,
    secure_cookies: bool
) -> APIRouter:
    router = APIRouter()

    generate_login_endpoint(router, route_dependencies.db, access_token_manager, samesite, secure_cookies)
    generate_authentication_endpoint(router, route_dependencies.current_user)
    generate_logout_endpoint(router, route_dependencies.validated_access_token, access_token_manager)
    generate_password_reset_link_endpoint(router, route_dependencies.db)
    generate_password_reset_endpoint(router, route_dependencies.db)

    parent_router.include_router(router)
    return router
