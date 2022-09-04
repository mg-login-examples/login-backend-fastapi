import logging

from fastapi import FastAPI

from core.cors_settings import add_cors
from api import routes as api_routes
from admin_app.mount_admin_app import mount_admin_app
from password_reset_app.mount_password_reset_app import mount_password_reset_app
from core.helper_classes.settings import Settings
from core.helper_classes.sqlAlchemyDBManager import SQLAlchemyDBManager
from core.route_dependencies import get_api_routes_dependencies, get_admin_routes_dependencies
from core.swagger_docs import create_swagger_docs_for_user_endpoints, create_swagger_docs_for_admin_endpoints
from core.token_store_manager import get_api_token_store_manager

logger = logging.getLogger(__name__)

def create_app(app_db_manager: SQLAlchemyDBManager, SETTINGS: Settings) -> FastAPI:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    user_access_token_manager = get_api_token_store_manager(SETTINGS, is_admin=False)
    admin_access_token_manager = get_api_token_store_manager(SETTINGS, is_admin=True)

    api_routes_dependencies = get_api_routes_dependencies(app_db_manager, user_access_token_manager)
    admin_api_routes_dependencies = get_admin_routes_dependencies(app_db_manager, admin_access_token_manager)
    api_router = api_routes.get_router(
        api_routes_dependencies,
        admin_api_routes_dependencies,
        SETTINGS.add_admin_app,
        SETTINGS.samesite,
        SETTINGS.secure_cookies,
    )
    app.include_router(api_router)

    if SETTINGS.add_admin_app:
        mount_admin_app(app)
    if SETTINGS.add_password_reset_app:
        mount_password_reset_app(app)

    add_cors(app, SETTINGS.cors_origins_set)

    create_swagger_docs_for_user_endpoints(app, api_routes_dependencies, SETTINGS.samesite, SETTINGS.secure_cookies)
    create_swagger_docs_for_admin_endpoints(app, admin_api_routes_dependencies, SETTINGS.secure_cookies)

    return app
