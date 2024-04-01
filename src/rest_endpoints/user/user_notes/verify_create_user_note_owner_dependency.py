import logging

from fastapi import Depends

from data.mongo_schemas.user_notes.user_note_create import UserNoteCreate
from data.schemas.http_error_exceptions.http_403_exceptions import \
    HTTP_403_NOT_AUTHORIZED_EXCEPTION
from data.schemas.users.user import User

logger = logging.getLogger(__name__)


def get_verify_create_user_note_owner_as_fastapi_dependency(
    get_current_user_as_dependency: User,
):
    def verify_create_user_note_owner(
        user_note_to_create: UserNoteCreate,
        current_user: User = get_current_user_as_dependency,
    ):
        if current_user.id != user_note_to_create.user_id:
            raise HTTP_403_NOT_AUTHORIZED_EXCEPTION

    return Depends(verify_create_user_note_owner)
