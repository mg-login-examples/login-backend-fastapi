from data.schemas.movies.movieDeep import Movie as MovieDeepSchema
from data.schemas.movies.movieAsModel import MovieAsModel as MovieAsModelSchema

def movieUpdateSchemaToMovieDict(movie: MovieDeepSchema) -> MovieAsModelSchema:
    movie_as_model = MovieAsModelSchema(**movie.dict(exclude={'book'}))
    if movie.book:
        movie_as_model.book_id = movie.book.id
    return movie_as_model

