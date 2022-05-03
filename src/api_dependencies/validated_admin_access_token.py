import logging

from fastapi import Depends, HTTPException, status
from fastapi.requests import Request
from data.access_tokens_store.access_token_manager import AccessTokenManager

logger = logging.getLogger(__name__)

def get_validated_admin_access_token_as_fastapi_dependency(
    token_extractor_as_fastapi_dependency: str,
    admin_access_token_manager: AccessTokenManager
):
    def validated_admin_access_token(request: Request, access_token: str = token_extractor_as_fastapi_dependency):
        try:
            if admin_access_token_manager.check_if_access_token_is_valid(access_token):
                return access_token
        except Exception as e:
            logger.error("Admin Access token validation error:")
            logger.error(f"Endpoint accessed: {request.url}")
            logger.error(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid access token")

    return Depends(validated_admin_access_token)
