from api_dependencies.user_route_dependencies import UserRouteDependencies
from helpers_classes.custom_api_router import APIRouter

from .resend_verification_email_endpoint import \
    generate_endpoint as generate_resend_email_endpoint
from .verify_email_endpoint import \
    generate_endpoint as generate_verify_email_endpoint


def get_router(user_route_dependencies: UserRouteDependencies) -> APIRouter:
    router = APIRouter(prefix="/email-verifications")

    generate_resend_email_endpoint(
        router,
        user_route_dependencies.sql_db_session,
        user_route_dependencies.current_user,
    )

    generate_verify_email_endpoint(
        router,
        user_route_dependencies.sql_db_session,
        user_route_dependencies.current_user,
    )

    return router
