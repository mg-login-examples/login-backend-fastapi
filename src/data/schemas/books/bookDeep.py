from typing import List

from data.schemas.books.book import Book as BookShallow
from data.schemas.movies.movie import Movie
from data.schemas.users.user import User

class Book(BookShallow):
    id: int
    movies: List[Movie] = []
    users: List[User] = []

    def get_class_by_field(field):
        if field == "movies":
            return Movie
        if field == "users":
            return User
        return None
