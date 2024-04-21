import logging

import pytest

from core.helper_classes.settings import Settings

# from core import logging_settings

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session", autouse=True)
def set_logging_level(app_settings: Settings):
    logger.info(f"Set test log level: {app_settings.log_level}")
    # logging.basicConfig(level=app_settings.log_level)
    # logging_settings.set_logging_settings(app_settings.log_level, app_settings.log_to_file, app_settings.log_filename)
