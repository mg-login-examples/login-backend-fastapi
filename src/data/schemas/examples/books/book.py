from data.schemas.examples.books.bookBase import BookBase
from pydantic import ConfigDict


class Book(BookBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
