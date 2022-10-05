from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql import func

from data.database.models.base import Base

class UserEmailVerification(Base):
    __tablename__ = "user_email_verifications"

    id = Column(Integer, primary_key=True, index=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    verification_code = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user = relationship("User", backref=backref("email_verifications", cascade="all,delete"))
    expires_at = Column(DateTime, nullable=False)
