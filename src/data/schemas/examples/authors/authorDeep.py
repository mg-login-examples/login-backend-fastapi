from data.schemas.examples.authors.author import Author as AuthorShallow
from data.schemas.examples.books.book import Book

class Author(AuthorShallow):
    id: int
    books: list[Book] = []

    def get_class_by_field(field):
        if field == "books":
            return Book
        return None

