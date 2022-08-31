from pydantic import BaseModel

class UserSessionBase(BaseModel):
    user_id: str
