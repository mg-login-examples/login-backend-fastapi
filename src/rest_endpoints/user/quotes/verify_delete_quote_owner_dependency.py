import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from data.database.models.quote import Quote as QuoteModel
from data.schemas.users.user import User
from stores.sql_db_store import crud_base

logger = logging.getLogger(__name__)

def get_verify_delete_quote_owner_as_fastapi_dependency(
    db_as_dependency: Session,
    get_current_user_as_dependency: User
):
    def verify_delete_quote_owner(
        item_id: int,
        current_user: User = get_current_user_as_dependency,
        db: Session = db_as_dependency
    ):
        quote_db = crud_base.get_resource_item(db, QuoteModel, item_id)
        if quote_db:
            quote_author = User(**quote_db.author.__dict__)
            if current_user.id == quote_author.id:
                return
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")

    return Depends(verify_delete_quote_owner)
