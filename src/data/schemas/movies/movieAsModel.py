from typing import Optional

from data.schemas.movies.movie import Movie as MovieShallow

class MovieAsModel(MovieShallow):
    id: int
    book_id: Optional[int] = None
