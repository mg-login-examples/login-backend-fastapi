import logging

from fastapi import Depends, HTTPException, status, Response
from fastapi.requests import Request

from data.access_tokens_store.helper_classes.access_token_store import AccessTokenStore

logger = logging.getLogger(__name__)

def get_validated_access_token_as_fastapi_dependency(
    token_extractor_as_fastapi_dependency: str,
    access_token_store_as_dependency: AccessTokenStore
):
    async def validated_access_token(
        request: Request,
        response: Response,
        access_token: str = token_extractor_as_fastapi_dependency,
        access_token_store: AccessTokenStore = access_token_store_as_dependency
    ):
        try:
            resp = await access_token_store.check_if_access_token_is_valid(access_token)
            if (resp):
                return access_token
        except Exception as e:
            logger.error("Access token validation error:")
            logger.error(f"Endpoint accessed: {request.url}")
            logger.error(e)
        response.delete_cookie("Authorization")
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid access token")

    return Depends(validated_access_token)
