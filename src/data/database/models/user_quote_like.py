from sqlalchemy import Integer, Column, ForeignKey, UniqueConstraint, DateTime
from sqlalchemy.sql import func

from data.database.models.base import Base
from data.database.models.user import User
from data.database.models.quote import Quote


class UserQuoteLike(Base):
    __tablename__ = "user_quote_likes"
    user_id = Column(Integer, ForeignKey(
        User.id, ondelete="CASCADE"), primary_key=True)
    quote_id = Column(Integer, ForeignKey(
        Quote.id, ondelete="CASCADE"), primary_key=True)
    __table_args__ = (
        UniqueConstraint('user_id', 'quote_id', name='_user_quote_uc'),
    )
    time_created = Column(DateTime(timezone=True), server_default=func.now())
