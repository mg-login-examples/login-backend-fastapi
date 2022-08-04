from data.schemas.quotes.quoteBase import QuoteBase

class Quote(QuoteBase):
    id: int

    class Config:
        orm_mode = True
