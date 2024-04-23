from data.schemas.examples.movies.movie import Movie as MovieShallow


class MovieAsModel(MovieShallow):
    id: int
    book_id: int | None = None
