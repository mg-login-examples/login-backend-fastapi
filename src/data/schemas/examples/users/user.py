from pydantic import ConfigDict

from data.schemas.examples.users.userBase import UserBase


class User(UserBase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
