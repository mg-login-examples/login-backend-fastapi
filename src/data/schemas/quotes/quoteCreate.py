from data.schemas.quotes.quoteBase import QuoteBase
from data.schemas.users.user import User

class QuoteCreate(QuoteBase):
    author: User
