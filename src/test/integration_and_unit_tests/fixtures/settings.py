import pytest
import logging
import os

from core.environment_settings import get_environment_settings
from core.helper_classes.settings import Settings

logger = logging.getLogger(__name__)

@pytest.fixture(scope="session")
def app_settings() -> Settings:
    dot_env_file = os.getenv("ENV_FILE", ".test.env")
    settings = get_environment_settings(dot_env_file=dot_env_file)
    logger.info(f"Test environment file selected: {dot_env_file}")
    logger.info("app settings:\n")
    for field in settings.dict():
        logger.info(f"{field}={settings.dict()[field]}")
    logger.info("\n")
    return settings