from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from data.database.models.base import Base

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    summary = Column(String)
    duration = Column(Integer)
    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("Book", back_populates="movies")
