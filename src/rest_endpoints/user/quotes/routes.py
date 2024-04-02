from api_dependencies.user_route_dependencies import UserRouteDependencies
from crud_endpoints_generator.crud_endpoints_generator import (
    generate_router_with_resource_endpoints,
)
from crud_endpoints_generator.endpoints_configs import EndpointsConfigs
from crud_endpoints_generator.resource_configurations import ResourceConfigurations
from data.database.models.quote import Quote as QuoteModel
from data.endUserSchemasToDbSchemas.quote import (
    createSchemaToDbSchema as quoteCreateSchemaToDbSchema,
)
from data.endUserSchemasToDbSchemas.quote import (
    updateSchemaToDbSchema as quoteUpdateSchemaToDbSchema,
)
from data.schemas.quotes.quoteCreate import QuoteCreate as QuoteCreateSchema
from data.schemas.quotes.quoteDeep import Quote as QuoteSchema
from helpers_classes.custom_api_router import APIRouter

from .edit_quote_text_endpoint import generate_endpoint as generate_edit_quote_endpoint
from .like_quote_endpoints import generate_endpoints as generate_like_quote_endpoints
from .verify_create_quote_owner_dependency import (
    get_verify_create_quote_owner_as_fastapi_dependency,
)
from .verify_delete_quote_owner_dependency import (
    get_verify_delete_quote_owner_as_fastapi_dependency,
)
from .verify_edit_quote_owner_dependency import (
    get_verify_edit_quote_owner_as_fastapi_dependency,
)


def get_router(user_route_dependencies: UserRouteDependencies) -> APIRouter:
    quote_resource_configurations = ResourceConfigurations(
        "quotes",
        QuoteSchema,
        QuoteCreateSchema,
        QuoteModel,
        customEndUserCreateSchemaToDbSchema=quoteCreateSchemaToDbSchema,
        customEndUserUpdateSchemaToDbSchema=quoteUpdateSchemaToDbSchema,
    )
    endpoints_required = EndpointsConfigs()
    endpoints_required.require_get_items()
    verify_create_quote_owner_dependency = (
        get_verify_create_quote_owner_as_fastapi_dependency(
            user_route_dependencies.current_user
        )
    )
    endpoints_required.require_post_item(
        dependencies=[verify_create_quote_owner_dependency]
    )
    verify_delete_quote_owner_dependency = (
        get_verify_delete_quote_owner_as_fastapi_dependency(
            user_route_dependencies.sql_db_session, user_route_dependencies.current_user
        )
    )
    endpoints_required.require_delete_item(
        dependencies=[verify_delete_quote_owner_dependency]
    )

    router = generate_router_with_resource_endpoints(
        endpoints_required,
        quote_resource_configurations,
        user_route_dependencies.sql_db_session,
        user_route_dependencies.mongo_db,
    )

    verify_edit_quote_owner_dependency = (
        get_verify_edit_quote_owner_as_fastapi_dependency(
            user_route_dependencies.sql_db_session, user_route_dependencies.current_user
        )
    )
    generate_edit_quote_endpoint(
        router,
        user_route_dependencies.sql_db_session,
        verify_edit_quote_owner_dependency,
    )

    generate_like_quote_endpoints(
        router,
        user_route_dependencies.sql_db_session,
        user_route_dependencies.restrict_endpoint_to_own_resources_param_user_id,
    )

    return router
