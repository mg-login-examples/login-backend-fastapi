from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import EmailType

from data.database.models.base import Base

class AdminUser(Base):
    __tablename__ = "admin_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(EmailType, unique=True, index=True)
    hashed_password = Column(String(128))
