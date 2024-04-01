from data.schemas.examples.books.bookAsModel import \
    BookAsModel as BookAsModelSchema
from data.schemas.examples.books.bookDeep import Book as BookDeepSchema


def updateSchemaToDbSchema(book: BookDeepSchema) -> BookAsModelSchema:
    book_as_model = BookAsModelSchema(**book.model_dump(exclude={"author"}))
    if book.author:
        book_as_model.author_id = book.author.id
    return book_as_model
