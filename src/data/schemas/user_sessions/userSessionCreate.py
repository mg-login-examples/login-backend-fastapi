from datetime import datetime

from data.schemas.user_sessions.userSessionBase import UserSessionBase
from pydantic import ConfigDict


class UserSessionCreate(UserSessionBase):
    token: str
    expires_at: datetime
    model_config = ConfigDict(from_attributes=True)
