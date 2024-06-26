from data.schemas.examples.books.book import Book
from data.schemas.examples.users.user import User as UserShallow


class User(UserShallow):
    books: list[Book]

    def get_class_by_field(field):
        if field == "books":
            return Book
        return None
