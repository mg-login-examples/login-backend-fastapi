from api_dependencies.helper_classes.custom_api_router import APIRouter
from api_dependencies.helper_classes.dependencies import Dependencies

from crud_endpoints_generator.crud_endpoints_generator import generate_router_with_resource_endpoints
from crud_endpoints_generator.resource_configurations import ResourceConfigurations
from crud_endpoints_generator.endpoints_configs import EndpointsConfigs
from data.schemas.quotes.quoteDeep import Quote as QuoteSchema
from data.schemas.quotes.quoteCreate import QuoteCreate as QuoteCreateSchema
from data.database.models.quote import Quote as QuoteModel
from data.endUserSchemasToDbSchemas.quote import updateSchemaToDbSchema as quoteUpdateSchemaToDbSchema
from data.endUserSchemasToDbSchemas.quote import createSchemaToDbSchema as quoteCreateSchemaToDbSchema

def add_resource_quotes_routes(parent_router: APIRouter, route_dependencies: Dependencies) -> APIRouter:
    quote_resource_configurations = ResourceConfigurations(
        "quotes",
        QuoteSchema,
        QuoteCreateSchema,
        QuoteModel,
        customEndUserCreateSchemaToDbSchema = quoteCreateSchemaToDbSchema,
        customEndUserUpdateSchemaToDbSchema = quoteUpdateSchemaToDbSchema
    )
    endpoints_required = EndpointsConfigs()
    endpoints_required.require_get_items()
    endpoints_required.require_post_item(dependencies=[route_dependencies.current_user])
    endpoints_required.require_delete_item(dependencies=[route_dependencies.current_user])

    router = generate_router_with_resource_endpoints(
        endpoints_required,
        quote_resource_configurations,
        route_dependencies.db
    )

    parent_router.include_router(router)
    return parent_router
