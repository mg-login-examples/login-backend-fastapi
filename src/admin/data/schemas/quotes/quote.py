from admin.data.schemas.quotes.quoteBase import QuoteBase
from admin.data.schemas.users.user import User

class Quote(QuoteBase):
    id: int
    author: User

    class Config:
        orm_mode = True
