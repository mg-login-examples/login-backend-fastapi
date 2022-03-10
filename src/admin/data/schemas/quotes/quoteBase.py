from pydantic import BaseModel

class QuoteBase(BaseModel):
    text: str
