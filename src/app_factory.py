from fastapi import FastAPI
import logging

from settings.cors_settings import add_cors
from api.routes import router

logger = logging.getLogger(__name__)

def create_app():
    app = FastAPI()
    add_cors(app)
    app.include_router(router)
    return app
