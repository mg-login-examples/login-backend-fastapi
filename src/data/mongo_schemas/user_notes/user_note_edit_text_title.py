from bson import ObjectId

from pydantic import ConfigDict, Field
from pydantic_mongo import ObjectIdField

from .user_note_base import UserNoteBase

class UserNote(UserNoteBase):
    id: ObjectIdField = Field(..., alias='_id')
    # TODO[pydantic]: The following keys were removed: `json_encoders`.
    # Check https://docs.pydantic.dev/dev-v2/migration/#changes-to-config for more information.
    model_config = ConfigDict(populate_by_name=True, json_encoders={
        ObjectId: str
    })
