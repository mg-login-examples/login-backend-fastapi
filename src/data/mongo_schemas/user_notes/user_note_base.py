from pydantic import BaseModel

class UserNoteBase(BaseModel):
    user_id: int
    title: str
    text: str
