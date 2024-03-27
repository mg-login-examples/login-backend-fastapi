import pytest
import logging
import os

from test.env_settings_test import EnvSettingsTest

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def env_settings_test() -> EnvSettingsTest:
    dot_env_file = os.getenv("ENV_FILE", ".test.env")
    settings = EnvSettingsTest(_env_file=dot_env_file)
    logger.info("test settings:\n")
    for field in settings.model_dump():
        logger.info(f"{field}={settings.model_dump()[field]}")
    logger.info("\n")
    return settings
