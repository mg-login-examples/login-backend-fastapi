import logging

from fastapi import Depends, HTTPException, status
from fastapi.requests import Request

from .helper_classes.cookie_extractor_for_oauth2_password import CookieExtractorWithOpenApiSecuritySchemeForOAuth2PasswordBearer
from data.in_memory_db.access_tokens import check_if_access_token_is_valid

logger = logging.getLogger(__name__)

def get_validated_access_token_as_fastapi_dependency(
    token_extractor_as_fastapi_dependency: str
):
    def validated_access_token(request: Request, access_token: str = token_extractor_as_fastapi_dependency):
        try:
            if check_if_access_token_is_valid(access_token):
                return access_token
        except Exception as e:
            logger.error("Access token validation error:")
            logger.error(f"Endpoint accessed: {request.url}")
            logger.error(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid access token")

    return Depends(validated_access_token)
