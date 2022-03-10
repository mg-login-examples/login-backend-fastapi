from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint

from data.database.models.base import Base
from data.database.models.user import User
from data.database.models.quote import Quote


user_liked_quotes = Table(
    'user_liked_quotes',
    Base.metadata,
    Column('user_id', ForeignKey(User.id)),
    Column('quote_id', ForeignKey(Quote.id)),
    UniqueConstraint('user_id', 'quote_id', name='uix_1'),
)
