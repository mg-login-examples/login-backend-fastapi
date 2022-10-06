import logging

from fastapi import Depends, HTTPException, status
from pymongo.database import Database

from data.mongo_schemas.user_notes.user_note_db_table import UserNoteDBTable
from data.mongo_schemas.user_notes.user_note import UserNote
from data.schemas.users.user import User
from stores.nosql_db_store import crud_base

logger = logging.getLogger(__name__)

def get_verify_delete_user_note_owner_as_fastapi_dependency(
    db_as_dependency: Database,
    get_current_user_as_dependency: User
):
    def verify_delete_quote_owner(
        user_note_id: str,
        current_user: User = get_current_user_as_dependency,
        db: Database = db_as_dependency,
    ):
        user_note_db: UserNote = crud_base.get_resource_item_by_id(db, UserNoteDBTable, user_note_id, UserNote)
        if user_note_db:
            if current_user.id == user_note_db.user_id:
                return
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")

    return Depends(verify_delete_quote_owner)
