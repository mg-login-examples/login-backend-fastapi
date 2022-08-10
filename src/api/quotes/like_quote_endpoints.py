import logging

from fastapi import status, Response
from sqlalchemy.orm import Session
from sqlite3 import IntegrityError

from api_dependencies.helper_classes.custom_api_router import APIRouter
from crud_endpoints_generator import crud_base
from data.schemas.users.user import User
from data.database.models.user_quote_like import UserQuoteLike as UserQuoteLikesModel
from data.schemas.user_quote_like.user_quote_like import UserQuoteLike

logger = logging.getLogger(__name__)

def generate_endpoints(
    router: APIRouter,
    db_as_dependency: Session,
    current_user_as_dependency: User
):
    @router.put("/{quote_id}/users/{user_id}/like/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[current_user_as_dependency])
    def like_quote(
        quote_id: int,
        user_id: int,
        db: Session = db_as_dependency
    ):
        user_quote_like = UserQuoteLike(user_id=user_id, quote_id=quote_id)
        try:
            user_quote_like = crud_base.create_resource_item(db, UserQuoteLikesModel, user_quote_like)
        except IntegrityError as _:
            pass
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.delete("/{quote_id}/users/{user_id}/like/", status_code=status.HTTP_204_NO_CONTENT, dependencies=[current_user_as_dependency])
    def unlike_quote(
        quote_id: int,
        user_id: int,
        db: Session = db_as_dependency
    ):
        attributes_and_values = [
            (UserQuoteLikesModel.quote_id, quote_id),
            (UserQuoteLikesModel.user_id, user_id),
        ]
        crud_base.delete_resource_item_by_attributes(db, UserQuoteLikesModel, attributes_and_values)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
