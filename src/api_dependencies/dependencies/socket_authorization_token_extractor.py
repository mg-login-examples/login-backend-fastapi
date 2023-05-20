import logging

from fastapi import WebSocket, Depends
from fastapi.security.utils import get_authorization_scheme_param
from data.schemas.http_error_exceptions.http_403_exceptions import HTTP_403_NOT_AUTHENTICATED_EXCEPTION

logger = logging.getLogger(__name__)

def get_socket_authorization_token_as_fastapi_dependency():
    def get_authorization_token(webSocket: WebSocket):
        header_authorization: str = webSocket.headers.get("Authorization")
        cookie_authorization: str = webSocket.cookies.get("Authorization")

        header_scheme, header_param = get_authorization_scheme_param(
            header_authorization
        )
        cookie_scheme, cookie_param = get_authorization_scheme_param(
            cookie_authorization
        )

        if header_scheme.lower() == "bearer":
            authorization = True
            param = header_param

        elif cookie_scheme.lower() == "bearer":
            authorization = True
            param = cookie_param

        else:
            authorization = False

        if not authorization:
            logger.error(f'Improper authorization error. Endpoint accessed: {webSocket.url}. Header Authorization: {header_authorization}. Cookie Authorization: {cookie_authorization}')
            raise HTTP_403_NOT_AUTHENTICATED_EXCEPTION
        return param

    return Depends(get_authorization_token)
