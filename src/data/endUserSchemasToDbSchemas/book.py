from data.schemas.books.bookDeep import Book as BookDeepSchema
from data.schemas.books.bookAsModel import BookAsModel as BookAsModelSchema

def updateSchemaToDbSchema(book: BookDeepSchema) -> BookAsModelSchema:
    book_as_model = BookAsModelSchema(**book.dict(exclude={'author'}))
    if book.author:
        book_as_model.author_id = book.author.id
    return book_as_model
