from typing import List

from fastapi import APIRouter
from sqlalchemy.orm import Session

from crud_endpoints_generator import crud_base
from data.schemas.users.user import User
from data.database.models.quote import Quote as QuoteModel
from data.schemas.quotes.quoteDeep import Quote as QuoteDeep

def generate_endpoint(
    router: APIRouter,
    current_user_as_dependency: User,
    db_as_dependency: Session
):
    @router.get("/{user_id}/quotes/", response_model=List[QuoteDeep])
    def get_user_quotes(
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        current_user: User = current_user_as_dependency,
        db: Session = db_as_dependency
    ):
        userQuotes = crud_base.get_resource_items_by_attribute(db, QuoteModel, QuoteModel.author_id, user_id, skip=skip, limit=limit)
        return userQuotes
