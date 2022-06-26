from fastapi import FastAPI

from api_dependencies.helper_classes.custom_api_router import APIRouter
from admin.api.routes import add_all_admin_resources_routes
from api.non_admin_routes import add_non_admin_routes
from api_dependencies.helper_classes.dependencies import Dependencies
from data.access_tokens_store.access_token_manager import AccessTokenManager

def add_routes(
    app: FastAPI,
    api_routes_dependencies: Dependencies,
    admin_routes_dependencies: Dependencies,
    user_access_token_manager: AccessTokenManager,
    admin_access_token_manager: AccessTokenManager,
    add_admin_app: bool
) -> FastAPI:
    api_router = APIRouter(prefix="/api")

    if add_admin_app:
        add_all_admin_resources_routes(api_router, admin_routes_dependencies, admin_access_token_manager)

    add_non_admin_routes(api_router, api_routes_dependencies, user_access_token_manager)

    app.include_router(api_router)
    
    return app
