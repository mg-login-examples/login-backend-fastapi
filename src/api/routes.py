from fastapi import APIRouter

from api.items import routes as items_routes
from api.items_personal import routes as items_personal_routes

router = APIRouter(prefix="/api")

router.include_router(items_routes.router)
router.include_router(items_personal_routes.router)
