from typing import List, Optional

from admin.data.schemas.examples.books.book import Book as BookShallow
from admin.data.schemas.examples.authors.author import Author
from admin.data.schemas.examples.movies.movie import Movie
from admin.data.schemas.examples.users.user import User

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
