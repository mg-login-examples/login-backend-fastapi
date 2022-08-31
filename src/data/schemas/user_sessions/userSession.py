from datetime import datetime

from data.schemas.user_sessions.userSessionBase import UserSessionBase

class UserSession(UserSessionBase):
    id: int
    expires_at: datetime

    class Config:
        orm_mode = True
