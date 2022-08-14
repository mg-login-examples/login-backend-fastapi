from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import EmailType

from data.database.models.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    email = Column(EmailType, unique=True, index=True)
    hashed_password = Column(String(128))
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    quotes = relationship("Quote", back_populates="author")
    liked_quotes = relationship(
        "Quote",
        secondary="user_quote_likes",
        back_populates="liked_by_users"
    )
