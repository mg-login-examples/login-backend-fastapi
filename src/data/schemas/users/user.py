from pydantic import ConfigDict

from data.schemas.users.userBase import UserBase


class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool
    name: str | None = None
    profile_picture: str | None = None
    model_config = ConfigDict(from_attributes=True)
