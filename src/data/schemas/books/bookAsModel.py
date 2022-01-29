from typing import List, Optional

from data.schemas.books.book import Book as BookShallow
from data.schemas.movies.movie import Movie
from data.schemas.users.user import User

class BookAsModel(BookShallow):
    id: int
    author_id: Optional[int] = None
    movies: List[Movie] = []
    users: List[User] = []
