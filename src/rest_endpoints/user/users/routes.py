from helpers_classes.custom_api_router import APIRouter
from crud_endpoints_generator.crud_endpoints_generator import generate_router_with_resource_endpoints
from crud_endpoints_generator.resource_configurations import ResourceConfigurations
from crud_endpoints_generator.endpoints_configs import EndpointsConfigs
from data.schemas.users.user import User as UserSchema
from data.schemas.users.userCreate import UserCreate as UserCreateSchema
from data.database.models.user import User as UserModel
from api_dependencies.common_route_dependencies import CommonRouteDependencies
from .create_user_endpoint import generate_endpoint as generate_create_user_endpoint
from .user_quotes_endpoint import generate_endpoint as generate_user_quotes_endpoint
from .user_sessions_endpoint import generate_endpoint as generate_user_sessions_endpoint

def get_router(
    api_dependencies: CommonRouteDependencies,
    samesite: str,
    secure_cookies: bool
) -> APIRouter:
    user_resource_configurations = ResourceConfigurations(
        "users",
        UserSchema,
        UserCreateSchema,
        UserModel
    )
    endpoints_required = EndpointsConfigs()
    endpoints_required.require_get_item(dependencies=[api_dependencies.restrict_endpoint_to_own_resources_param_item_id])

    router = generate_router_with_resource_endpoints(
        endpoints_required,
        user_resource_configurations,
        api_dependencies.db
    )

    generate_create_user_endpoint(
        router,
        api_dependencies.db,
        api_dependencies.access_token_store,
        samesite,
        secure_cookies
    )

    generate_user_quotes_endpoint(
        router,
        api_dependencies.db,
        api_dependencies.restrict_endpoint_to_own_resources_param_user_id,
    )

    generate_user_sessions_endpoint(
        router,
        api_dependencies.db,
        api_dependencies.restrict_endpoint_to_own_resources_param_user_id,
    )

    return router
