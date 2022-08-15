from pydantic import BaseModel

class AdminLoginResponse(BaseModel):
    id: int
    email: str
    access_token: str
    token_type: str
