from fastapi import HTTPException, status

HTTP_403_NOT_AUTHENTICATED_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
)
HTTP_403_NOT_AUTHORIZED_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not authorized to access this resource",
)
HTTP_403_INVALID_TOKEN_EXCEPTION = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail="Invalid access token"
)
