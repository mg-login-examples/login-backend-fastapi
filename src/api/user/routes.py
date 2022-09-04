from api_dependencies.helper_classes.custom_api_router import APIRouter
from api.user.authentication import routes as authentication_routes
from api.user.users import routes as users_routes
from api.user.quotes import routes as quotes_routes
from api.user.email_verification import routes as email_verifications_routes
from api_dependencies.helper_classes.dependencies import Dependencies

def get_router(
    dependencies: Dependencies,
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
