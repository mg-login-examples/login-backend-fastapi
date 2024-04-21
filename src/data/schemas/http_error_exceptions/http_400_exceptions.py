from fastapi import HTTPException, status

HTTP_400_BAD_REQUEST_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid request"
)
HTTP_400_INVALID_PASSWORD_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid password"
)
HTTP_400_ITEM_ID_MISMATCH_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Item id in request body different from path parameter",
)
HTTP_400_INVALID_IMAGE_TYPE_EXCEPTION = HTTPException(
    status_code=400,
    detail="Invalid file type. Only PNG and JPEG/JPG files are allowed.",
)
