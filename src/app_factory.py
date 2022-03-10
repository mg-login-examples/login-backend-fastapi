import logging

from fastapi import FastAPI

from settings.cors_settings import add_cors
from api.routes import router
from admin.view.mount_admin_app import mount_admin_app

logger = logging.getLogger(__name__)

def create_app():
    app = FastAPI()
    add_cors(app)
    app.include_router(router)
    mount_admin_app(app)
    return app
