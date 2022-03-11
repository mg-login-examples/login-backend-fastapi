from typing import List

from data.schemas.examples.users.user import User as UserShallow
from data.schemas.examples.books.book import Book

class User(UserShallow):
    books: List[Book]

    def get_class_by_field(field):
        if field == "books":
            return Book
        return None
