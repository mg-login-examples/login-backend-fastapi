import logging

from fastapi import Response

from helpers_classes.custom_api_router import APIRouter
from data.schemas.admin_users.admin_user import AdminUser

logger = logging.getLogger(__name__)


def generate_endpoint(
    router: APIRouter,
    current_user_dependency: AdminUser
):
    @router.post("/authenticate/", response_model=AdminUser)
    def authenticate_user(
        response: Response,
        user: AdminUser = current_user_dependency
    ):
        return user
