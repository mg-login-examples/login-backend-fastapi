from pydantic import ConfigDict

from data.schemas.examples.books.bookBase import BookBase


class Book(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
