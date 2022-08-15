from datetime import datetime
from pydantic import BaseModel

class UserEmailVerificationBase(BaseModel):
    verification_code: int
    user_id: int
    expires_at: datetime
