import logging

from fastapi import Response, status

from api_dependencies.helper_classes.custom_api_router import APIRouter
from data.access_tokens_store.access_token_manager import AccessTokenManager
from utils.security.access_token_utils import parse_access_token

logger = logging.getLogger(__name__)

def generate_endpoint(
    router: APIRouter,
    validated_access_token_as_fastapi_dependency: str,
    access_token_manager: AccessTokenManager,
):
    @router.post("/logout/", status_code=status.HTTP_200_OK)
    def logout_user(
        response: Response,
        validated_access_token: str = validated_access_token_as_fastapi_dependency
    ):
        user_id = parse_access_token(validated_access_token, "user_id")
        access_token_manager.remove_access_token(user_id, validated_access_token)
        response.delete_cookie("Admin-Authorization")
        return None
