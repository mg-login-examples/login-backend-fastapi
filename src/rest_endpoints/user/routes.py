from api_dependencies.user_route_dependencies import UserRouteDependencies
from helpers_classes.custom_api_router import APIRouter
from rest_endpoints.user.authentication import routes as authentication_routes
from rest_endpoints.user.email_verification import routes as email_verifications_routes
from rest_endpoints.user.quotes import routes as quotes_routes
from rest_endpoints.user.user_notes import routes as user_notes_routes
from rest_endpoints.user.users import routes as users_routes


def get_router(
    user_route_dependencies: UserRouteDependencies, auth_cookie_type: str
) -> APIRouter:
    router = APIRouter()

    authentication_router = authentication_routes.get_router(
        user_route_dependencies, auth_cookie_type
    )
    router.include_router(authentication_router)

    users_router = users_routes.get_router(user_route_dependencies, auth_cookie_type)
    router.include_router(users_router)

    quotes_router = quotes_routes.get_router(user_route_dependencies)
    router.include_router(quotes_router)

    email_verifications_router = email_verifications_routes.get_router(
        user_route_dependencies
    )
    router.include_router(email_verifications_router)

    user_notes_router = user_notes_routes.get_router(user_route_dependencies)
    router.include_router(user_notes_router)

    return router
