from bson import ObjectId

from pydantic import ConfigDict, Field
from pydantic_mongo import ObjectIdField

from .user_note_base import UserNoteBase


class UserNote(UserNoteBase):
    id: ObjectIdField = Field(..., alias='_id')
    model_config = ConfigDict(populate_by_name=True, json_encoders={
        ObjectId: str
    })
