from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint

from data.database.models.base import Base

user_book_table = Table('user_book', Base.metadata,
    Column('user_id', ForeignKey('users.id')),
    Column('book_id', ForeignKey('books.id')),
    UniqueConstraint('user_id', 'book_id', name='uix_1'),
)
