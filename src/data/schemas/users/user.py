from typing import Optional

from data.schemas.users.userBase import UserBase

class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    name: Optional[str]
    profile_picture: Optional[str]

    class Config:
        orm_mode = True
