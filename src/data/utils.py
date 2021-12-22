from data.schemas import users as userSchemas
from data.database.models.user import User as UserModel

def userCreateSchemaToUserModel(user: userSchemas.UserCreate) -> UserModel:
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = UserModel(email=user.email, hashed_password=fake_hashed_password)
    return db_user
