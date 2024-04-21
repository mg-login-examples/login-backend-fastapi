from pydantic import ConfigDict

from data.schemas.quotes.quoteBase import QuoteBase
from data.schemas.users.user import User


class Quote(QuoteBase):
    id: int
    author: User
    model_config = ConfigDict(from_attributes=True)
