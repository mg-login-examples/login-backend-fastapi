from fastapi import HTTPException, status

HTTP_500_UNEXPECTED_EXCEPTION = HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected internal error")
