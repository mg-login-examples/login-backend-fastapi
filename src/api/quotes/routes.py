from fastapi import APIRouter
from api_dependencies.helper_classes.dependencies import Dependencies

from crud_endpoints_generator.crud_endpoints_generator import generate_router_with_resource_endpoints
from crud_endpoints_generator.resource_configurations import ResourceConfigurations
from crud_endpoints_generator.endpoints_required import Endpoints
from data.schemas.quotes.quoteDeep import Quote as QuoteSchema
from data.schemas.quotes.quoteCreate import QuoteCreate as QuoteCreateSchema
from data.database.models.quote import Quote as QuoteModel
from data.endUserSchemasToDbSchemas.quote import updateSchemaToDbSchema as quoteUpdateSchemaToDbSchema
from data.endUserSchemasToDbSchemas.quote import createSchemaToDbSchema as quoteCreateSchemaToDbSchema

def add_resource_quotes_routes(
    parent_router: APIRouter,
    route_dependencies: Dependencies
) -> APIRouter:
    quote_resource_configurations = ResourceConfigurations(
        "quotes",
        QuoteSchema,
        QuoteCreateSchema,
        QuoteModel,
        customEndUserCreateSchemaToDbSchema = quoteCreateSchemaToDbSchema,
        customEndUserUpdateSchemaToDbSchema = quoteUpdateSchemaToDbSchema
    )
    endpoints_required = Endpoints().require_get_items().require_post_item().require_delete_item()

    router = generate_router_with_resource_endpoints(
        endpoints_required,
        quote_resource_configurations,
        route_dependencies
    )

    parent_router.include_router(router)
    return parent_router
