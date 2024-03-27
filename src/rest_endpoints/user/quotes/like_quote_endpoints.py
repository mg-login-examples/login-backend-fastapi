import logging
from typing import Any

from fastapi import status, Response
from sqlalchemy.orm import Session
from sqlite3 import IntegrityError

from helpers_classes.custom_api_router import APIRouter
from stores.sql_db_store import crud_base
from data.database.models.user_quote_like import UserQuoteLike as UserQuoteLikesModel
from data.schemas.user_quote_like.user_quote_like import UserQuoteLike

logger = logging.getLogger(__name__)


def generate_endpoints(
    router: APIRouter,
    sql_db_session_as_dependency: Session,
    restrict_endpoint_to_own_resources_param_user_id_as_dependency: Any
):
    @router.put("/{quote_id}/users/{user_id}/like/", status_code=status.HTTP_204_NO_CONTENT,
                dependencies=[restrict_endpoint_to_own_resources_param_user_id_as_dependency])
    def like_quote(
        quote_id: int,
        user_id: int,
        sql_db_session: Session = sql_db_session_as_dependency
    ):
        user_quote_like = UserQuoteLike(user_id=user_id, quote_id=quote_id)
        try:
            user_quote_like = crud_base.create_resource_item(
                sql_db_session, UserQuoteLikesModel, user_quote_like)
        except IntegrityError as _:
            pass
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @router.delete("/{quote_id}/users/{user_id}/like/", status_code=status.HTTP_204_NO_CONTENT,
                   dependencies=[restrict_endpoint_to_own_resources_param_user_id_as_dependency])
    def unlike_quote(
        quote_id: int,
        user_id: int,
        sql_db_session: Session = sql_db_session_as_dependency
    ):
        attributes_and_values = [
            (UserQuoteLikesModel.quote_id, quote_id),
            (UserQuoteLikesModel.user_id, user_id),
        ]
        crud_base.delete_resource_item_by_attributes(
            sql_db_session, UserQuoteLikesModel, attributes_and_values)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
