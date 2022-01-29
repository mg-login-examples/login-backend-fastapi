from typing import List, Optional

from data.schemas.books.book import Book as BookShallow
from data.schemas.authors.author import Author
from data.schemas.movies.movie import Movie
from data.schemas.users.user import User

class Book(BookShallow):
    id: int
    author: Optional[Author] = None
    movies: List[Movie] = []
    users: List[User] = []

    def get_class_by_field(field):
        if field == "author":
            return Author
        if field == "movies":
            return Movie
        if field == "users":
            return User
        return None
