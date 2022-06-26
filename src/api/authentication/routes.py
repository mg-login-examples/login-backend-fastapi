from api_dependencies.helper_classes.custom_api_router import APIRouter

from api_dependencies.helper_classes.dependencies import Dependencies
from data.access_tokens_store.access_token_manager import AccessTokenManager

from .login_endpoint import generate_endpoint as generate_login_endpoint
from .authenticate_endpoint import generate_endpoint as generate_authentication_endpoint

def add_authentication_routes(
    parent_router: APIRouter,
    route_dependencies: Dependencies,
    access_token_manager: AccessTokenManager
) -> APIRouter:
    router = APIRouter()

    generate_login_endpoint(router, route_dependencies.db, access_token_manager)
    generate_authentication_endpoint(router, route_dependencies.current_user)

    parent_router.include_router(router)
    return router
