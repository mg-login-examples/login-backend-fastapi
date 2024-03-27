from fastapi import HTTPException, status

HTTP_410_EXPIRED_OR_INACTIVE_CODE_EXCEPTION = HTTPException(
    status_code=status.HTTP_410_GONE, detail="Expired or inactive code")
