from sqlalchemy import Integer, Column, ForeignKey, String, DateTime, Index
from sqlalchemy.sql import func

from data.database.models.base import Base
from data.database.models.user import User

class UserSession(Base):
    __tablename__ = "user_sessions"
    __table_args__ = (
        Index("idx_token", "token", mysql_length=1024),
    )
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String(1000), unique=True, index=True)
    expires_at = Column(DateTime, nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
