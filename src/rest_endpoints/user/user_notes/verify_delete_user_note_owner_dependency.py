import logging

from fastapi import Depends, HTTPException, status
from pymongo.database import Database

from data.mongo_schemas.user_notes.user_note import UserNote
from data.mongo_schemas.user_notes.user_note_db_table import UserNoteDBTable
from data.schemas.http_error_exceptions.http_403_exceptions import (
    HTTP_403_NOT_AUTHORIZED_EXCEPTION,
)
from data.schemas.users.user import User
from stores.nosql_db_store import crud_base

logger = logging.getLogger(__name__)


def get_verify_delete_user_note_owner_as_fastapi_dependency(
    mongo_db_as_dependency: Database, get_current_user_as_dependency: User
):
    def verify_delete_quote_owner(
        user_note_id: str,
        current_user: User = get_current_user_as_dependency,
        mongo_db: Database = mongo_db_as_dependency,
    ):
        user_note_db = crud_base.get_resource_item_by_id(
            mongo_db, UserNoteDBTable, user_note_id
        )
        if not user_note_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
            )
        user_note = UserNote(**user_note_db)

        if current_user.id != user_note.user_id:
            raise HTTP_403_NOT_AUTHORIZED_EXCEPTION

    return Depends(verify_delete_quote_owner)
