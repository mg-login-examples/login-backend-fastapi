from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from data.database.models.base import Base
from data.database.models.examples.user_book import user_book_table


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    summary = Column(String)
    number_of_pages = Column(Integer)
    movies = relationship("Movie", back_populates="book")
    users = relationship(
        "User",
        secondary=user_book_table,
        back_populates="books"
    )
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", back_populates="books")
