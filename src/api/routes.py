from fastapi import APIRouter

from api.items import routes as items_routes

router = APIRouter(prefix="/api")
router.include_router(items_routes.router, prefix="/items")
