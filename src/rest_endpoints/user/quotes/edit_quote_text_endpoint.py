from typing import Any

from fastapi import status, Response
from sqlalchemy.orm import Session

from helpers_classes.custom_api_router import APIRouter
from stores.sql_db_store import crud_base
from data.database.models.quote import Quote as QuoteModel
from data.schemas.quotes.quoteEditText import Quote as QuoteEditText
from data.schemas.http_error_exceptions.http_400_exceptions import HTTP_400_ITEM_ID_MISMATCH_EXCEPTION
from data.schemas.http_error_exceptions.http_404_exceptions import HTTP_404_ITEM_NOT_FOUND_EXCEPTION

def generate_endpoint(
    router: APIRouter,
    db_as_dependency: Session,
    verify_edit_quote_owner_dependency: Any
):
    @router.put("/{quote_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[verify_edit_quote_owner_dependency])
    def edit_quote_text(
        quote_id: int,
        quote: QuoteEditText,
        db: Session = db_as_dependency
    ):
        if quote_id != quote.id:
            raise HTTP_400_ITEM_ID_MISMATCH_EXCEPTION
        db_quote = crud_base.update_resource_item_partial(db, QuoteModel, quote)
        if not db_quote:
            raise HTTP_404_ITEM_NOT_FOUND_EXCEPTION
        return Response(status_code=status.HTTP_204_NO_CONTENT)
