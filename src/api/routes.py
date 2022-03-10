from fastapi import APIRouter

from admin.api import routes as admin_routes
from api.users import routes as user_routes
from api.quotes import routes as quote_routes

router = APIRouter(prefix="/api")

router.include_router(admin_routes.router)

router.include_router(user_routes.router)
router.include_router(quote_routes.router)
