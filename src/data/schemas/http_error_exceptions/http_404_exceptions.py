from fastapi import HTTPException, status

HTTP_404_ITEM_NOT_FOUND_EXCEPTION = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
