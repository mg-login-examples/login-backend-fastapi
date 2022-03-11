from admin.data.schemas.examples.users.userBase import UserBase

class UserCreateAsModel(UserBase):
    hashed_password: str
