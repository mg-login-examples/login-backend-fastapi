from pydantic import BaseModel

class LoginResponse(BaseModel):
    id: str
    email: str
    access_token: str
    token_type: str
