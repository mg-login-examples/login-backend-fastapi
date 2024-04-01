from pydantic import ConfigDict

from data.schemas.quotes.quoteBase import QuoteBase


class Quote(QuoteBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
