from datetime import datetime

from pydantic import ConfigDict

from data.schemas.user_sessions.userSessionBase import UserSessionBase


class UserSessionCreate(UserSessionBase):
    token: str
    expires_at: datetime
    model_config = ConfigDict(from_attributes=True)
