from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy_utils import EmailType
from sqlalchemy.sql import func

from data.database.models.base import Base

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    email = Column(EmailType, unique=True, index=True)
    hashed_password = Column(String(128))
