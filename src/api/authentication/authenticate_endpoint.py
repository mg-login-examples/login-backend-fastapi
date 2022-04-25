import logging

from fastapi import APIRouter, Response
from data.schemas.users.user import User

logger = logging.getLogger(__name__)

def generate_endpoint(
    router: APIRouter,
    current_user_dependency: User
):
    @router.post("/authenticate/", response_model=User)
    def authenticate_user(
        response: Response,
        user: User = current_user_dependency
    ):
        return user