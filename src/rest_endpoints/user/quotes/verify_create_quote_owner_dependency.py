import logging

from fastapi import Depends

from data.schemas.quotes.quoteCreate import QuoteCreate
from data.schemas.users.user import User
from data.schemas.http_error_exceptions.http_403_exceptions import HTTP_403_NOT_AUTHORIZED_EXCEPTION

logger = logging.getLogger(__name__)


def get_verify_create_quote_owner_as_fastapi_dependency(
    get_current_user_as_dependency: User
):
    def verify_create_quote_owner(
        item: QuoteCreate,
        current_user: User = get_current_user_as_dependency,
    ):
        if current_user.id != item.author.id:
            raise HTTP_403_NOT_AUTHORIZED_EXCEPTION

    return Depends(verify_create_quote_owner)
