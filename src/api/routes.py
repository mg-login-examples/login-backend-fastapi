from typing import Callable
from fastapi import APIRouter, FastAPI

from admin.api.routes import add_all_admin_resources_routes
from api.authentication.routes import add_authentication_routes
from api.users.routes import add_resource_users_routes
from api.quotes.routes import add_resource_quotes_routes
from api_dependencies.helper_classes.dependencies import Dependencies

def add_routes(app: FastAPI, get_db_session: Callable, route_dependencies: Dependencies, add_admin_app: bool) -> FastAPI:
    api_router = APIRouter(prefix="/api")

    if add_admin_app:
        add_all_admin_resources_routes(api_router, get_db_session)

    add_authentication_routes(api_router, get_db_session, route_dependencies)
    add_resource_users_routes(api_router, get_db_session)
    add_resource_quotes_routes(api_router, get_db_session)

    app.include_router(api_router)
    return app
