from typing import Optional

from pydantic import ConfigDict

from data.schemas.users.userBase import UserBase


class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    name: Optional[str]
    profile_picture: Optional[str]
    model_config = ConfigDict(from_attributes=True)
