from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from data.database.models.base import Base
from data.database.models.examples.user_book import user_book_table


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    books = relationship("Book", secondary=user_book_table, back_populates="users")
