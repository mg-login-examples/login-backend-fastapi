from api_dependencies.user_route_dependencies import UserRouteDependencies
from helpers_classes.custom_api_router import APIRouter

from .authenticate_endpoint import \
    generate_endpoint as generate_authentication_endpoint
from .google_login_endpoint import \
    generate_endpoint as generate_google_login_endpoint
from .login_endpoint import generate_endpoint as generate_login_endpoint
from .logout_endpoint import generate_endpoint as generate_logout_endpoint
from .password_change_endpoint import \
    generate_endpoint as generate_password_change_endpoint
from .password_reset_endpoint import \
    generate_endpoint as generate_password_reset_endpoint
from .password_reset_link_endpoint import \
    generate_endpoint as generate_password_reset_link_endpoint


def get_router(
    user_route_dependencies: UserRouteDependencies,
    auth_cookie_type: str,
) -> APIRouter:
    router = APIRouter()

    generate_login_endpoint(
        router,
        user_route_dependencies.sql_db_session,
        user_route_dependencies.access_token_store,
        auth_cookie_type,
    )
    generate_authentication_endpoint(router, user_route_dependencies.current_user)
    generate_logout_endpoint(
        router,
        user_route_dependencies.sql_db_session,
        user_route_dependencies.access_token_store,
        user_route_dependencies.validated_access_token,
    )
    generate_password_reset_link_endpoint(
        router, user_route_dependencies.sql_db_session
    )
    generate_password_reset_endpoint(router, user_route_dependencies.sql_db_session)
    generate_password_change_endpoint(
        router,
        user_route_dependencies.sql_db_session,
        user_route_dependencies.access_token_store,
        user_route_dependencies.current_user,
        auth_cookie_type,
    )
    generate_google_login_endpoint(
        router,
        user_route_dependencies.sql_db_session,
        user_route_dependencies.access_token_store,
        auth_cookie_type,
    )

    return router
