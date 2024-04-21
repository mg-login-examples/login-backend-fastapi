from datetime import datetime

from pydantic import ConfigDict

from data.schemas.user_sessions.userSessionBase import UserSessionBase


class UserSession(UserSessionBase):
    id: int
    expires_at: datetime
    model_config = ConfigDict(from_attributes=True)
