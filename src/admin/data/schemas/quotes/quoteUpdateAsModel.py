from typing import List

from admin.data.schemas.quotes.quoteBase import QuoteBase
from admin.data.schemas.users.user import User

class QuoteUpdateAsModel(QuoteBase):
    id: int
    author_id: int
    liked_by_users: List[User]
