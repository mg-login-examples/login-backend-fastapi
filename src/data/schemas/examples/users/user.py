from data.schemas.examples.users.userBase import UserBase

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
