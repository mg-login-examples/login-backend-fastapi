import logging

from fastapi import FastAPI

from core.cors_settings import add_cors
from api.routes import add_routes
from admin.view.mount_admin_app import mount_admin_app
from core.helper_classes.settings import Settings
from core.helper_classes.sqlAlchemyDBManager import SQLAlchemyDBManager
from core.route_dependencies import get_api_routes_dependencies, get_admin_routes_dependencies
from core.swagger_docs import create_swagger_docs_for_regular_endpoints, create_swagger_docs_for_admin_endpoints
from data.access_tokens_store.access_token_manager import AccessTokenManager

logger = logging.getLogger(__name__)

def create_app(app_db_manager: SQLAlchemyDBManager, SETTINGS: Settings) -> FastAPI:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    # TODO Redis store for access tokens
    user_access_token_manager = AccessTokenManager(store_type="file", file_name="user_access_tokens.txt")
    admin_access_token_manager = AccessTokenManager(store_type="file", file_name="admin_access_tokens.txt")
    api_routes_dependencies = get_api_routes_dependencies(app_db_manager, user_access_token_manager)
    admin_api_routes_dependencies = get_admin_routes_dependencies(app_db_manager, admin_access_token_manager)
    add_routes(
        app,
        api_routes_dependencies,
        admin_api_routes_dependencies,
        user_access_token_manager,
        admin_access_token_manager,
        SETTINGS.add_admin_app
    )

    if SETTINGS.add_admin_app:
        mount_admin_app(app)

    add_cors(app, SETTINGS.cors_origins_set)

    create_swagger_docs_for_regular_endpoints(app, api_routes_dependencies, user_access_token_manager)
    create_swagger_docs_for_admin_endpoints(app, admin_api_routes_dependencies, admin_access_token_manager)

    return app
