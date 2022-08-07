from fastapi import status, HTTPException, Response
from sqlalchemy.orm import Session

from api_dependencies.helper_classes.custom_api_router import APIRouter
from crud_endpoints_generator import crud_base
from data.schemas.users.user import User
from data.database.models.quote import Quote as QuoteModel
from data.schemas.quotes.quoteEditText import Quote as QuoteEditText

def generate_endpoint(
    router: APIRouter,
    db_as_dependency: Session,
    current_user_as_dependency: User
):
    @router.put("/{quote_id}/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[current_user_as_dependency])
    def edit_quote_text(
        quote_id: int,
        quote: QuoteEditText,
        db: Session = db_as_dependency
    ):
        if quote_id != quote.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item id in request body different from path parameter")
        db_quote = crud_base.update_resource_item_partial(db, QuoteModel, quote)
        if not db_quote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
        return Response(status_code=status.HTTP_204_NO_CONTENT)