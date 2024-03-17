from typing import List

from data.schemas.users.user import User as UserShallow
from data.schemas.quotes.quote import Quote

class User(UserShallow):
    quotes: List[Quote]
    liked_quotes: List[Quote]

    @staticmethod
    def get_class_by_field(field: str):
        """
        used by admin app to determine foreign key class from json schemas
        """
        if field == "quotes":
            return Quote
        if field == "liked_quotes":
            return Quote
        raise Exception(f'Unknown field provided {field}')
