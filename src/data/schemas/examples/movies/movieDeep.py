from data.schemas.examples.books.book import Book
from data.schemas.examples.movies.movie import Movie as MovieShallow


class Movie(MovieShallow):
    id: int
    book: Book | None = None

    def get_class_by_field(field):
        if field == "book":
            return Book
        return None
