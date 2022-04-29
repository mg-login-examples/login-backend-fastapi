import logging

from fastapi import FastAPI

from core.cors_settings import add_cors
from api.routes import add_routes
from admin.view.mount_admin_app import mount_admin_app
from core.helper_classes.settings import Settings
from core.helper_classes.sqlAlchemyDBManager import SQLAlchemyDBManager
from core.route_dependencies import get_api_routes_dependencies, get_admin_routes_dependencies

logger = logging.getLogger(__name__)

def create_app(app_db_manager: SQLAlchemyDBManager, SETTINGS: Settings) -> FastAPI:
    app = FastAPI()

    add_cors(app, SETTINGS.cors_origins_set)

    api_routes_dependencies = get_api_routes_dependencies(app_db_manager)
    admin_api_routes_dependencies = get_admin_routes_dependencies(app_db_manager)
    add_routes(app, api_routes_dependencies, admin_api_routes_dependencies, SETTINGS.add_admin_app)

    if SETTINGS.add_admin_app:
        mount_admin_app(app)

    return app
