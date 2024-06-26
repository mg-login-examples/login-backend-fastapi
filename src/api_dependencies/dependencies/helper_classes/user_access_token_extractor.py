import logging

from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param

from data.schemas.http_error_exceptions.http_403_exceptions import (
    HTTP_403_NOT_AUTHENTICATED_EXCEPTION,
)

logger = logging.getLogger(__name__)


class UserAccessTokenExtractor(OAuth2PasswordBearer):
    """OAuth2 password flow with token in a httpOnly cookie."""

    async def __call__(self, request: Request) -> str | None:
        """Extract and return a token from the request cookies.
        Raises:
            HTTPException: 403 error if no token cookie is present.
        """
        header_authorization: str | None = request.headers.get("Authorization")
        cookie_authorization: str | None = request.cookies.get("Authorization")

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
            logger.error(
                f"Improper authorization error. Endpoint accessed: {request.url}. Header Authorization: {header_authorization}. Cookie Authorization: {cookie_authorization}"
            )
            raise HTTP_403_NOT_AUTHENTICATED_EXCEPTION
        return param
