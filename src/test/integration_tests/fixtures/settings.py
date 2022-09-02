import pytest
import logging
import os

from core.environment_settings import get_environment_settings
from core.helper_classes.settings import Settings
from test.env_settings_test import EnvSettingsTest

logger = logging.getLogger(__name__)

@pytest.fixture
def app_settings() -> Settings:
    dot_env_file = os.getenv("ENV_FILE", ".test.env")
    settings = get_environment_settings(dot_env_file=dot_env_file)
    logger.debug(f"Test environment file selected: {dot_env_file}")
    return settings

@pytest.fixture
def env_settings_test() -> EnvSettingsTest:
    dot_env_file = os.getenv("ENV_FILE", ".test.env")
    settings = EnvSettingsTest(_env_file=dot_env_file)
    return settings
