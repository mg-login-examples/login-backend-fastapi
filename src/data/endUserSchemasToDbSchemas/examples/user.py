from data.schemas.examples.users.userCreate import \
    UserCreate as UserCreateSchema
from data.schemas.examples.users.userCreateAsModel import \
    UserCreateAsModel as UserCreateAsModelSchema


def createSchemaToDbSchema(user: UserCreateSchema) -> UserCreateAsModelSchema:
    fake_hashed_password = user.password + "notreallyhashed"
    user_as_model = UserCreateAsModelSchema(
        email=user.email, hashed_password=fake_hashed_password
    )
    return user_as_model
