from datetime import datetime
from pydantic import BaseModel

class UserPasswordResetTokenBase(BaseModel):
    token: str
    user_id: int
    expires_at: datetime
