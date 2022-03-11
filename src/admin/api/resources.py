from typing import List

from crud_endpoints_generator.resource_configurations import ResourceConfigurations

from data.database.models.user import User as UserModel
from data.schemas.users.userDeep import User as UserSchema
from data.schemas.users.userCreate import UserCreate as UserCreateSchema
from data.endUserSchemasToDbSchemas.user import createSchemaToDbSchema as userCreateSchemaToDbSchema

from data.database.models.quote import Quote as QuoteModel
from data.schemas.quotes.quoteDeep import Quote as QuoteSchema
from data.schemas.quotes.quoteCreate import QuoteCreate as QuoteCreateSchema
from data.endUserSchemasToDbSchemas.quote import createSchemaToDbSchema as quoteCreateSchemaToDbSchema
from data.endUserSchemasToDbSchemas.quote import updateSchemaToDbSchema as quoteUpdateSchemaToDbSchema

resourcesConfigurations: List[ResourceConfigurations] = [
    ResourceConfigurations(
        "users",
        UserSchema,
        UserCreateSchema,
        UserModel,
        customEndUserCreateSchemaToDbSchema=userCreateSchemaToDbSchema,
    ),
    ResourceConfigurations(
        "quotes",
        QuoteSchema,
        QuoteCreateSchema,
        QuoteModel,
        customEndUserCreateSchemaToDbSchema=quoteCreateSchemaToDbSchema,
        customEndUserUpdateSchemaToDbSchema=quoteUpdateSchemaToDbSchema,
    ),
]

if not len({resourceConfiguration.resource_endpoints_url_prefix for resourceConfiguration in resourcesConfigurations}) == len(resourcesConfigurations):
    raise ValueError("2 or more Admin resources have the same url prefix! Ensure all url prefix are unique.")
