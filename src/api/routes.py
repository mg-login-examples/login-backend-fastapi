from fastapi import APIRouter

from api.admin import routes as admin_routes

router = APIRouter(prefix="/api")

router.include_router(admin_routes.router)
