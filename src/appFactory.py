from fastapi import FastAPI
from core.settings import settings
from core.cors_settings import add_cors
from api.routes import router

def create_app():
    app = FastAPI()

    add_cors(app)

    app.include_router(router)

    return app
