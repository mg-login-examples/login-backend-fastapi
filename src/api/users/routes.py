from crud_endpoints_generator.crud_endpoints_generator import get_resource_endpoints_router
from crud_endpoints_generator.resource_configurations import ResourceConfigurations
from crud_endpoints_generator.endpoints_required import Endpoints
from data.schemas.users.user import User as UserSchema
from data.schemas.users.userCreate import UserCreate as UserCreateSchema
from data.database.models.user import User as UserModel
from data.endUserSchemasToDbSchemas.user import createSchemaToDbSchema as userCreateSchemaToDbSchema
from app_configurations import app_db_manager

user_resource_configurations = ResourceConfigurations(
    "users",
    UserSchema,
    UserCreateSchema,
    UserModel,
    customEndUserCreateSchemaToDbSchema = userCreateSchemaToDbSchema
)
endpoints_required = Endpoints().require_get_item().require_post_item()

router = get_resource_endpoints_router(
    endpoints_required,
    user_resource_configurations,
    app_db_manager.db_session
)
