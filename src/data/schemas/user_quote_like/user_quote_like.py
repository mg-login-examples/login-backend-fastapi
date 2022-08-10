from pydantic import BaseModel

class UserQuoteLike(BaseModel):
    user_id: int
    quote_id: int
