from typing import List

from data.schemas.quotes.quote import Quote as QuoteShallow
from data.schemas.users.user import User

class Quote(QuoteShallow):
    liked_by_users: List[User]

    @staticmethod
    def get_class_by_field(field: str):
        if field == "author":
            return User
        if field == "liked_by_users":
            return User
        return None
