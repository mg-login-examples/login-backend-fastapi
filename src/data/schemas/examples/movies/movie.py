from admin.data.schemas.examples.movies.movieBase import MovieBase

class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True
