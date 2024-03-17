from typing import Optional

from data.schemas.examples.books.book import Book as BookShallow
from data.schemas.examples.authors.author import Author
from data.schemas.examples.movies.movie import Movie
from data.schemas.examples.users.user import User

class Book(BookShallow):
    id: int
    author: Optional[Author] = None
    movies: list[Movie] = []
    users: list[User] = []

    def get_class_by_field(field):
        if field == "author":
            return Author
        if field == "movies":
            return Movie
        if field == "users":
            return User
        return None
