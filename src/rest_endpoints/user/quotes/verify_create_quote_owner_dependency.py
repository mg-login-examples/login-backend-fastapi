import logging

from fastapi import Depends, HTTPException, status

from data.schemas.quotes.quoteCreate import QuoteCreate
from data.schemas.users.user import User

logger = logging.getLogger(__name__)

def get_verify_create_quote_owner_as_fastapi_dependency(
    get_current_user_as_dependency: User
):
    def verify_create_quote_owner(
        item: QuoteCreate,
        current_user: User = get_current_user_as_dependency,
    ):
        if current_user.id != item.author.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to access this resource")

    return Depends(verify_create_quote_owner)
