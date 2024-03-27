from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from data.database.models.base import Base


class Quote(Base):
    __tablename__ = "quotes"

    id = Column(Integer, primary_key=True, index=True)
    time_created = Column(DateTime(timezone=True), server_default=func.now())
    time_updated = Column(DateTime(timezone=True), onupdate=func.now())
    text = Column(String(1000))
    author_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)

    author = relationship("User", back_populates="quotes")
    liked_by_users = relationship(
        "User",
        secondary="user_quote_likes",
        back_populates="liked_quotes",
    )
