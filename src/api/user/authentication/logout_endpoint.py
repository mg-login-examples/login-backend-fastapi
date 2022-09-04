import logging

from fastapi import Response, status
from sqlalchemy.orm import Session

from api_dependencies.helper_classes.custom_api_router import APIRouter
from data.access_tokens_store.helper_classes.access_token_store import AccessTokenStore
from utils.security.access_token_utils import parse_access_token
from crud_endpoints_generator import crud_base
from data.database.models.user_session import UserSession as UserSessionModel

logger = logging.getLogger(__name__)

def generate_endpoint(
    router: APIRouter,
    db_as_dependency: Session,
    access_token_store_as_dependency: AccessTokenStore,
    validated_access_token_as_fastapi_dependency: str,
):
    @router.post("/logout/", status_code=status.HTTP_200_OK)
    async def logout_user(
        response: Response,
        db: Session = db_as_dependency,
        access_token_store: AccessTokenStore = access_token_store_as_dependency,
        validated_access_token: str = validated_access_token_as_fastapi_dependency,
    ):
        user_id = parse_access_token(validated_access_token, "user_id")
        crud_base.delete_resource_item_by_attribute(db, UserSessionModel, UserSessionModel.token, validated_access_token)
        await access_token_store.remove_access_token(user_id, validated_access_token)

        response.delete_cookie("Authorization")
        return None
