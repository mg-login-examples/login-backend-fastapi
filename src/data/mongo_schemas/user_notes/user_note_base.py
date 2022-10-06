from pydantic import BaseModel

class UserNoteBase(BaseModel):
    title: str
    text: str
