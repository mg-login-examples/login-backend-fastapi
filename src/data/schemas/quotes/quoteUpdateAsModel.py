from data.schemas.quotes.quoteBase import QuoteBase
from data.schemas.users.user import User

class QuoteUpdateAsModel(QuoteBase):
    id: int
    author_id: int
    liked_by_users: list[User]
