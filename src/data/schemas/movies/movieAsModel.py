from typing import Optional

from data.schemas.movies.movie import Movie as MovieShallow
from data.schemas.books.book import Book

class MovieAsModel(MovieShallow):
    id: int
    book_id: Optional[int] = None
