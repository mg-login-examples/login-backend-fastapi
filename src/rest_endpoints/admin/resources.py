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

from data.mongo_schemas.user_notes.user_note import UserNote as UserNoteSchema
from data.mongo_schemas.user_notes.user_note_create import UserNoteCreate as UserNoteCreateSchema
from data.mongo_schemas.user_notes.user_note_db_table import UserNoteDBTable

resources_configurations: list[ResourceConfigurations] = [
    ResourceConfigurations(
        "users",
        UserSchema,
        UserCreateSchema,
        ResourceModel=UserModel,
        customEndUserCreateSchemaToDbSchema=userCreateSchemaToDbSchema,
    ),
    ResourceConfigurations(
        "quotes",
        QuoteSchema,
        QuoteCreateSchema,
        ResourceModel=QuoteModel,
        customEndUserCreateSchemaToDbSchema=quoteCreateSchemaToDbSchema,
        customEndUserUpdateSchemaToDbSchema=quoteUpdateSchemaToDbSchema,
    ),
    ResourceConfigurations(
        "user-notes",
        UserNoteSchema,
        UserNoteCreateSchema,
        MongoDBTable=UserNoteDBTable,
    ),
]

if len({resource_configuration.resource_endpoints_url_prefix for resource_configuration in resources_configurations}
       ) != len(resources_configurations):
    raise ValueError(
        "2 or more Admin resources have the same url prefix! Ensure all url prefix are unique.")
