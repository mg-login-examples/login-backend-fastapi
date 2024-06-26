import logging

from fastapi import Response, status
from sqlalchemy.orm import Session

from data.database.models.user_session import UserSession as UserSessionModel
from helpers_classes.custom_api_router import APIRouter
from stores.access_tokens_store.access_token_store import AccessTokenStore
from stores.sql_db_store import crud_base
from utils.security.access_token_utils import parse_access_token

logger = logging.getLogger(__name__)


def generate_endpoint(
    router: APIRouter,
    sql_db_session_as_dependency: Session,
    access_token_store_as_dependency: AccessTokenStore,
    validated_access_token_as_fastapi_dependency: str,
):
    @router.post("/logout/", status_code=status.HTTP_200_OK)
    async def logout_user(
        response: Response,
        sql_db_session: Session = sql_db_session_as_dependency,
        access_token_store: AccessTokenStore = access_token_store_as_dependency,
        validated_access_token: str = validated_access_token_as_fastapi_dependency,
    ):
        user_id = parse_access_token(validated_access_token, "user_id")
        crud_base.delete_resource_item_by_attribute(
            sql_db_session,
            UserSessionModel,
            UserSessionModel.token,
            validated_access_token,
        )
        await access_token_store.remove_access_token(user_id, validated_access_token)

        response.delete_cookie("Authorization")
        return None
