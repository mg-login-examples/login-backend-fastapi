from bson import ObjectId

from pydantic import Field

from data.mongo_schemas.helper_classes.py_object_id import PyObjectId
from .user_note_base import UserNoteBase

class UserNote(UserNoteBase):
    id: PyObjectId = Field(..., alias='_id')
    user_id: int

    class Config:
        # arbitrary_types_allowed = True
        allow_population_by_field_name = True
        json_encoders = {
            ObjectId: str
        }
