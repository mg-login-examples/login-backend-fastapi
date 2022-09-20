from api_dependencies.helper_classes.custom_api_router import APIRouter
from rest_endpoints.admin import routes as admin_routes
from rest_endpoints.user import routes as user_routes
from api_dependencies.helper_classes.dependencies import Dependencies

def get_router(
    api_routes_dependencies: Dependencies,
    admin_routes_dependencies: Dependencies,
    add_admin_app: bool,
    samesite: str,
    secure_cookies: bool,
) -> APIRouter:
    api_router = APIRouter(prefix="/api")

    if add_admin_app:
        admin_router = admin_routes.get_router(admin_routes_dependencies, secure_cookies)
        api_router.include_router(admin_router)

    user_router = user_routes.get_router(api_routes_dependencies, samesite, secure_cookies)
    api_router.include_router(user_router)

    return api_router    
