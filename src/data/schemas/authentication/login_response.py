from pydantic import BaseModel
from data.schemas.users.user import User

class LoginResponse(BaseModel):
    user: User
    access_token: str
    token_type: str
