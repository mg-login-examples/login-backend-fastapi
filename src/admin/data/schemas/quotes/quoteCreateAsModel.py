from typing import List

from admin.data.schemas.quotes.quoteBase import QuoteBase

class QuoteCreateAsModel(QuoteBase):
    author_id: int
