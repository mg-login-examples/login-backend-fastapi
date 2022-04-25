from pydantic import BaseModel

class LoginResponseModel(BaseModel):
    id: str
    email: str
    access_token: str
    token_type: str
