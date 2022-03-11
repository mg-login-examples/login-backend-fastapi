from typing import Optional

from admin.data.schemas.examples.movies.movie import Movie as MovieShallow
from admin.data.schemas.examples.books.book import Book

class Movie(MovieShallow):
    id: int
    book: Optional[Book] = None

    def get_class_by_field(field):
        if field == "book":
            return Book
        return None
