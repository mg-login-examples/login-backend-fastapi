from admin.data.schemas.quotes.quoteBase import QuoteBase
from admin.data.schemas.users.user import User

class QuoteCreate(QuoteBase):
    author: User
