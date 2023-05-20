from fastapi import HTTPException, status

HTTP_401_INVALID_LOGIN_EXCEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect login")
HTTP_401_GOOGLE_LOGIN_UNVERIFIED_EMAIL_EXCEPTION = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Google email not verified")
