from data.schemas.users.userBase import UserBase

class UserCreate(UserBase):
    password: str
