from typing import List, Optional

from data.schemas.examples.books.book import Book as BookShallow
from data.schemas.examples.movies.movie import Movie
from data.schemas.examples.users.user import User

class BookAsModel(BookShallow):
    author_id: Optional[int] = None
    movies: List[Movie] = []
    users: List[User] = []
