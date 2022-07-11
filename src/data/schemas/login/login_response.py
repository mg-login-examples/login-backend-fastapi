from pydantic import BaseModel

class LoginResponse(BaseModel):
    id: int
    email: str
    access_token: str
    token_type: str
