from data.schemas.users.userCreate import UserCreate as UserCreateSchema
from data.schemas.users.userCreateAsModel import UserCreateAsModel as UserCreateAsModelSchema
from utils.security.password_utils import get_password_hash

def createSchemaToDbSchema(user: UserCreateSchema) -> UserCreateAsModelSchema:
    hashed_password = get_password_hash(user.password)
    user_as_model = UserCreateAsModelSchema(email=user.email, hashed_password=hashed_password)
    return user_as_model
