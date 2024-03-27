from data.schemas.users.userBase import UserBase


class UserCreateAsModel(UserBase):
    hashed_password: str
