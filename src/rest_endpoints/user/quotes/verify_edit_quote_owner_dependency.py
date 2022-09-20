import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from data.database.models.quote import Quote as QuoteModel
from data.schemas.quotes.quoteEditText import Quote as QuoteEditText
from data.schemas.users.user import User
from crud_endpoints_generator import crud_base

logger = logging.getLogger(__name__)

def get_verify_edit_quote_owner_as_fastapi_dependency(
    db_as_dependency: Session,
    get_current_user_as_dependency: User
):
    def verify_edit_quote_owner(
        quote: QuoteEditText,
        current_user: User = get_current_user_as_dependency,
        db: Session = db_as_dependency
    ):
        quote_db = crud_base.get_resource_item(db, QuoteModel, quote.id)
        if not quote_db:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        quote_author = User(**quote_db.author.__dict__)
        if current_user.id != quote_author.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")

    return Depends(verify_edit_quote_owner)
