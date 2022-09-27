from bson import ObjectId

from pydantic import Field

from data.mongo_schemas.helper_classes.py_object_id import PyObjectId
from .user_notes_base import UserNotesBase

class UserNotes(UserNotesBase):
    id: PyObjectId = Field(..., alias='_id')

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
