from api_dependencies.helper_classes.custom_api_router import APIRouter
from api_dependencies.helper_classes.dependencies import Dependencies
from .resend_verification_email_endpoint import generate_endpoint as generate_resend_email_endpoint
from .verify_email_endpoint import generate_endpoint as generate_verify_email_endpoint

def add_resource_email_verifications_routes(parent_router: APIRouter, api_dependencies: Dependencies) -> APIRouter:
    router = APIRouter(prefix="/email-verifications")

    generate_resend_email_endpoint(
        router,
        api_dependencies.db,
        api_dependencies.current_user
    )

    generate_verify_email_endpoint(
        router,
        api_dependencies.db,
        api_dependencies.current_user
    )

    parent_router.include_router(router)
    return parent_router
