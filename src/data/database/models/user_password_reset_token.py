from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from data.database.models.base import Base


class UserPasswordResetToken(Base):
    __tablename__ = "user_password_reset_tokens"

    id = Column(Integer, primary_key=True, index=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    token = Column(String(128), nullable=False)
    is_active = Column(Boolean, default=False, nullable=False)
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    expires_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="user_password_reset_tokens")
