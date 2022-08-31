import pytest
import logging
import os

import requests
from fastapi.testclient import TestClient

from core.environment_settings import get_environment_settings
from core.helper_classes.settings import Settings
from core.db_manager import get_db_manager
from core.helper_classes.sqlAlchemyDBManager import SQLAlchemyDBManager
from utils.db import dbUtils
from core.app_factory import create_app
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

@pytest.fixture
def test_app_db_manager(app_settings: Settings):
    app_db_manager = get_db_manager(app_settings.database_url, app_settings.database_user, app_settings.database_password)
    return app_db_manager

@pytest.fixture
def setup_db(test_app_db_manager: SQLAlchemyDBManager):
    dbUtils.create_all_tables(test_app_db_manager.engine)

@pytest.fixture
def test_client(app_settings: Settings, test_app_db_manager: SQLAlchemyDBManager, setup_db) -> requests.Session:
    app = create_app(test_app_db_manager, app_settings)
    return TestClient(app)
