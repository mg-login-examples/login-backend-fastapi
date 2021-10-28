from fastapi import APIRouter

router = APIRouter()

@router.get("/for-all", tags=["items"])
async def get_public_items():
    return [{"id": 1, "name": "public item 1"}, {"id": 2, "name": "public item 2"}]

@router.get("/for-logged-in", tags=["items"])
async def get_private_items():
    return [{"id": 1, "name": "private item 1"}, {"id": 2, "name": "private item 2"}, {"id": 3, "name": "private item 3"}]
