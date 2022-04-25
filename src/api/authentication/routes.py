from typing import Callable
from fastapi import APIRouter

from api_dependencies.helper_classes.dependencies import Dependencies

from .login_endpoint import generate_endpoint as generate_login_endpoint
from .authenticate_endpoint import generate_endpoint as generate_authentication_endpoint

def add_authentication_routes(parent_router: APIRouter, get_db_session: Callable, route_dependencies: Dependencies) -> APIRouter:
    router = APIRouter()

    generate_login_endpoint(router, get_db_session)
    generate_authentication_endpoint(router, route_dependencies.current_user)

    parent_router.include_router(router)
    return router
