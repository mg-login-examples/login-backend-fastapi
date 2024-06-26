import logging

from fastapi import Response

from data.schemas.users.user import User
from helpers_classes.custom_api_router import APIRouter

logger = logging.getLogger(__name__)


def generate_endpoint(router: APIRouter, current_user_dependency: User):
    @router.post("/authenticate/", response_model=User)
    def authenticate_user(response: Response, user: User = current_user_dependency):
        return user
