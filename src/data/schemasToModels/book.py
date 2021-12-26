from data.schemas.books.bookDeep import Book as BookDeepSchema
from data.database.models.book import Book as BookModel

def bookUpdateSchemaToBookDict(book: BookDeepSchema) -> BookModel:
    book_dict = book.dict()
    if book.movies:
        book_dict["movies"] = [movie.id for movie in book.movies]
    if book.users:
        book_dict["users"] = [user.id for user in book.users]
    return book_dict
