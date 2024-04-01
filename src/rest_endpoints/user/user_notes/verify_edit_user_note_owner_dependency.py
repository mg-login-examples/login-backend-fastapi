import logging

from fastapi import Depends, HTTPException, status
from pymongo.database import Database

from data.mongo_schemas.user_notes.user_note_db_table import UserNoteDBTable
from data.mongo_schemas.user_notes.user_note_edit_text_title import (
    UserNote as UserNoteEditTitleText,
)
from data.mongo_schemas.user_notes.user_note import UserNote
from data.schemas.users.user import User
from stores.nosql_db_store import crud_base
from data.schemas.http_error_exceptions.http_403_exceptions import (
    HTTP_403_NOT_AUTHORIZED_EXCEPTION,
)

logger = logging.getLogger(__name__)


def get_verify_edit_user_note_owner_as_fastapi_dependency(
    mongo_db_as_dependency: Database, get_current_user_as_dependency: User
):
    def verify_edit_user_note_owner(
        user_note: UserNoteEditTitleText,
        current_user: User = get_current_user_as_dependency,
        mongo_db: Database = mongo_db_as_dependency,
    ):
        user_note_db = crud_base.get_resource_item_by_id(
            mongo_db, UserNoteDBTable, str(user_note.id)
        )
        if not user_note_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )
        user_note_actual = UserNote(**user_note_db)
        if current_user.id != user_note_actual.user_id:
            raise HTTP_403_NOT_AUTHORIZED_EXCEPTION

    return Depends(verify_edit_user_note_owner)
