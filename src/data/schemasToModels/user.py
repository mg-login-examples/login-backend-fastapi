from data.schemas.users.userCreate import UserCreate as UserCreateSchema
from data.schemas.users.userCreateAsModel import UserCreateAsModel as UserCreateAsModelSchema
from data.schemas.users.userDeep import User as UserDeepSchema
from data.database.models.user import User as UserModel


def userCreateSchemaToUserModel(user: UserCreateSchema) -> UserCreateAsModelSchema:
    fake_hashed_password = user.password + "notreallyhashed"
    user_as_model = UserCreateAsModelSchema(email=user.email, hashed_password=fake_hashed_password)
    return user_as_model
