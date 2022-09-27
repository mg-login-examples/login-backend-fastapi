from pydantic import BaseModel

class UserNotesBase(BaseModel):
    user_id: int
    title: str
    text: str
