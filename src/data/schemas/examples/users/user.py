from data.schemas.examples.users.userBase import UserBase
from pydantic import ConfigDict

class User(UserBase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)
