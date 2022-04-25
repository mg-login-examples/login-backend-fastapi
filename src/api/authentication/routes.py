from typing import Callable
from fastapi import APIRouter

from .login_endpoint import generate_endpoint as generate_login_endpoint

def add_authentication_routes(parent_router: APIRouter, get_db_session: Callable) -> APIRouter:
    router = APIRouter()

    generate_login_endpoint(router, get_db_session)

    parent_router.include_router(router)
    return router
