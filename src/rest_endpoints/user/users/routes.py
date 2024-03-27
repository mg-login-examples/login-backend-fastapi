from helpers_classes.custom_api_router import APIRouter
from crud_endpoints_generator.crud_endpoints_generator import generate_router_with_resource_endpoints
from crud_endpoints_generator.resource_configurations import ResourceConfigurations
from crud_endpoints_generator.endpoints_configs import EndpointsConfigs
from data.schemas.users.user import User as UserSchema
from data.schemas.users.userCreate import UserCreate as UserCreateSchema
from data.database.models.user import User as UserModel
from api_dependencies.user_route_dependencies import UserRouteDependencies
from .create_user_endpoint import generate_endpoint as generate_create_user_endpoint
from .get_users_endpoint import generate_endpoint as generate_get_users_endpoint
from .get_users_by_ids_endpoint import generate_endpoint as generate_get_users_by_ids_endpoint
from .user_profile_endpoints import generate_endpoints as generate_user_profile_endpoints
from .user_quotes_endpoint import generate_endpoint as generate_user_quotes_endpoint
from .user_sessions_endpoint import generate_endpoint as generate_user_sessions_endpoint
from .user_notes_endpoint import generate_endpoint as generate_user_notes_endpoint


def get_router(
    user_route_dependencies: UserRouteDependencies,
    auth_cookie_type: str
) -> APIRouter:
    user_resource_configurations = ResourceConfigurations(
        "users",
        UserSchema,
        UserCreateSchema,
        UserModel,
    )
    endpoints_required = EndpointsConfigs()
    endpoints_required.require_get_item(
        dependencies=[user_route_dependencies.restrict_endpoint_to_own_resources_param_item_id])

    router = generate_router_with_resource_endpoints(
        endpoints_required,
        user_resource_configurations,
        user_route_dependencies.sql_db_session,
        user_route_dependencies.mongo_db,
    )

    generate_create_user_endpoint(
        router,
        user_route_dependencies.sql_db_session,
        user_route_dependencies.access_token_store,
        auth_cookie_type
    )

    generate_get_users_endpoint(
        router,
        user_route_dependencies.sql_db_session,
        user_route_dependencies.current_user,
    )

    generate_get_users_by_ids_endpoint(
        router,
        user_route_dependencies.sql_db_session,
        user_route_dependencies.current_user,
    )

    generate_user_profile_endpoints(
        router,
        user_route_dependencies.sql_db_session,
        user_route_dependencies.current_user,
        user_route_dependencies.restrict_endpoint_to_own_resources_param_user_id
    )

    generate_user_quotes_endpoint(
        router,
        user_route_dependencies.sql_db_session,
        user_route_dependencies.restrict_endpoint_to_own_resources_param_user_id,
    )

    generate_user_sessions_endpoint(
        router,
        user_route_dependencies.sql_db_session,
        user_route_dependencies.restrict_endpoint_to_own_resources_param_user_id,
    )

    generate_user_notes_endpoint(
        router,
        user_route_dependencies.mongo_db,
        user_route_dependencies.restrict_endpoint_to_own_resources_param_user_id,
    )

    return router
