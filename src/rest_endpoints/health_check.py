import logging

from helpers_classes.custom_api_router import APIRouter

logger = logging.getLogger(__name__)


def generate_endpoint(
    router: APIRouter,
):
    @router.head("/health-check/")
    def health_check():
        return
