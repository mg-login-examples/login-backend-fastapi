from api_dependencies.helper_classes.custom_api_router import APIRouter
from api.authentication.routes import add_authentication_routes
from api.users.routes import add_resource_users_routes
from api.quotes.routes import add_resource_quotes_routes
from api.email_verification.routes import add_resource_email_verifications_routes
from api_dependencies.helper_classes.dependencies import Dependencies
from data.access_tokens_store.access_token_manager import AccessTokenManager

def add_non_admin_routes(
    parent_router: APIRouter,
    dependencies: Dependencies,
    access_token_manager: AccessTokenManager,
    samesite: str,
    secure_cookies: bool
) -> APIRouter:
    router = APIRouter()

    add_authentication_routes(router, dependencies, access_token_manager, samesite, secure_cookies)
    add_resource_users_routes(router, dependencies, access_token_manager, samesite, secure_cookies)
    add_resource_quotes_routes(router, dependencies)
    add_resource_email_verifications_routes(router, dependencies)

    parent_router.include_router(router)
    return parent_router
