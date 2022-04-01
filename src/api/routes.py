from typing import Callable
from fastapi import APIRouter, FastAPI

from admin.api.routes import add_all_admin_resources_routes
from api.users.routes import add_resource_users_routes
from api.quotes.routes import add_resource_quotes_routes

def add_routes(app: FastAPI, get_db_session: Callable, add_admin_app: bool) -> FastAPI:
    api_router = APIRouter(prefix="/api")

    if add_admin_app:
        add_all_admin_resources_routes(api_router, get_db_session)

    add_resource_users_routes(api_router, get_db_session)
    add_resource_quotes_routes(api_router, get_db_session)

    app.include_router(api_router)
    return app
