from data.schemas.examples.books.book import Book as BookShallow
from data.schemas.examples.movies.movie import Movie
from data.schemas.examples.users.user import User


class BookAsModel(BookShallow):
    author_id: int | None = None
    movies: list[Movie] = []
    users: list[User] = []
