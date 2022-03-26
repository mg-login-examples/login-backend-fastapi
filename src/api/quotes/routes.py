from crud_endpoints_generator.crud_endpoints_generator import get_resource_endpoints_router
from crud_endpoints_generator.resource_configurations import ResourceConfigurations
from crud_endpoints_generator.endpoints_required import Endpoints
from data.schemas.quotes.quoteDeep import Quote as QuoteSchema
from data.schemas.quotes.quoteCreate import QuoteCreate as QuoteCreateSchema
from data.database.models.quote import Quote as QuoteModel
from data.endUserSchemasToDbSchemas.quote import updateSchemaToDbSchema as quoteUpdateSchemaToDbSchema
from data.endUserSchemasToDbSchemas.quote import createSchemaToDbSchema as quoteCreateSchemaToDbSchema
from app_configurations import app_db_manager

user_resource_configurations = ResourceConfigurations(
    "quotes",
    QuoteSchema,
    QuoteCreateSchema,
    QuoteModel,
    customEndUserCreateSchemaToDbSchema = quoteCreateSchemaToDbSchema,
    customEndUserUpdateSchemaToDbSchema = quoteUpdateSchemaToDbSchema
)
endpoints_required = Endpoints().require_get_items().require_post_item().require_delete_item()

router = get_resource_endpoints_router(
    endpoints_required,
    user_resource_configurations,
    app_db_manager.db_session
)