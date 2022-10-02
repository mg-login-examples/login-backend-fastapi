import logging

from fastapi import Depends, HTTPException, status

from data.mongo_schemas.user_notes.user_note_create import UserNoteCreate
from data.schemas.users.user import User

logger = logging.getLogger(__name__)

def get_verify_create_user_note_owner_as_fastapi_dependency(
    get_current_user_as_dependency: User
):
    def verify_create_user_note_owner(
        user_note_to_create: UserNoteCreate,
        current_user: User = get_current_user_as_dependency,
    ):
        if current_user.id != user_note_to_create.user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")

    return Depends(verify_create_user_note_owner)
