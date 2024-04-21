import logging

from fastapi import Depends, WebSocket

from data.schemas.http_error_exceptions.http_403_exceptions import (
    HTTP_403_INVALID_TOKEN_EXCEPTION,
)
from stores.access_tokens_store.access_token_store import AccessTokenStore

logger = logging.getLogger(__name__)


def get_socket_validated_access_token_as_fastapi_dependency(
    token_extractor_as_fastapi_dependency: str,
    access_token_store_as_dependency: AccessTokenStore,
):
    async def validated_socket_access_token(
        webSocket: WebSocket,
        access_token: str = token_extractor_as_fastapi_dependency,
        access_token_store: AccessTokenStore = access_token_store_as_dependency,
    ):
        try:
            resp = await access_token_store.check_if_access_token_is_valid(access_token)
            if resp:
                return access_token
        except Exception as e:
            logger.error(
                f"Invalid access token error - Endpoint accessed: {webSocket.url}:"
            )
            logger.error(e)
        raise HTTP_403_INVALID_TOKEN_EXCEPTION

    return Depends(validated_socket_access_token)
