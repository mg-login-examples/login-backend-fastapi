from helpers_classes.custom_api_router import APIRouter
from rest_endpoints.user.authentication import routes as authentication_routes
from rest_endpoints.user.users import routes as users_routes
from rest_endpoints.user.quotes import routes as quotes_routes
from rest_endpoints.user.email_verification import routes as email_verifications_routes
from api_dependencies.common_route_dependencies import CommonRouteDependencies

def get_router(
    dependencies: CommonRouteDependencies,
    samesite: str,
    secure_cookies: bool
) -> APIRouter:
    router = APIRouter()

    authentication_router = authentication_routes.get_router(dependencies, samesite, secure_cookies)
    router.include_router(authentication_router)

    users_router = users_routes.get_router(dependencies, samesite, secure_cookies)
    router.include_router(users_router)

    quotes_router = quotes_routes.get_router(dependencies)
    router.include_router(quotes_router)

    email_verifications_router = email_verifications_routes.get_router(dependencies)
    router.include_router(email_verifications_router)

    return router
