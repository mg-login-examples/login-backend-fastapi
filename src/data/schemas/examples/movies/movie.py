from data.schemas.examples.movies.movieBase import MovieBase
from pydantic import ConfigDict

class Movie(MovieBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
