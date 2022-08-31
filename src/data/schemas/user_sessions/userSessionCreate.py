from datetime import datetime

from data.schemas.user_sessions.userSessionBase import UserSessionBase

class UserSessionCreate(UserSessionBase):
    token: str
    expires_at: datetime

    class Config:
        orm_mode = True
