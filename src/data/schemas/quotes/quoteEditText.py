from data.schemas.quotes.quoteBase import QuoteBase
from pydantic import ConfigDict


class Quote(QuoteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
