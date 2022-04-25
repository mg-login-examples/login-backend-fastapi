import logging

from fastapi import FastAPI

from core.cors_settings import add_cors
from api.routes import add_routes
from admin.view.mount_admin_app import mount_admin_app
from core.helper_classes.sqlAlchemyDBManager import SQLAlchemyDBManager

logger = logging.getLogger(__name__)

def create_app(app_db_manager: SQLAlchemyDBManager, add_admin_app: bool = False) -> FastAPI:
    app = FastAPI()
    add_cors(app)
    add_routes(app, app_db_manager.db_session, add_admin_app)
    if add_admin_app:
        mount_admin_app(app)
    return app