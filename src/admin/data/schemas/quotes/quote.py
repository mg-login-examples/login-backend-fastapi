from data.schemas.quotes.quoteBase import QuoteBase
from data.schemas.users.user import User

class Quote(QuoteBase):
    id: int
    author: User

    class Config:
        orm_mode = True
