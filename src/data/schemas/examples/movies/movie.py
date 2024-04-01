from pydantic import ConfigDict

from data.schemas.examples.movies.movieBase import MovieBase


class Movie(MovieBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
