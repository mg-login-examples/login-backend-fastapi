from typing import List

from data.schemas.authors.author import Author as AuthorShallow
from data.schemas.books.book import Book

class Author(AuthorShallow):
    id: int
    books: List[Book] = []

    def get_class_by_field(field):
        if field == "books":
            return Book
        return None

