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

logger = logging.getLogger(__name__)

@pytest.fixture
def test_settings() -> Settings:
    dot_env_file = os.getenv("ENV_FILE", ".env")
    SETTINGS = get_environment_settings(dot_env_file=dot_env_file)
    logger.info(f".env file selected: {dot_env_file}")
    return SETTINGS

@pytest.fixture
def test_app_db_manager(test_settings: Settings):
    app_db_manager = get_db_manager(test_settings.database_url, test_settings.database_user, test_settings.database_password)
    return app_db_manager

@pytest.fixture
def setup_db(test_app_db_manager: SQLAlchemyDBManager):
    dbUtils.create_all_tables(test_app_db_manager.engine)


@pytest.fixture
def test_client(test_settings: Settings, test_app_db_manager: SQLAlchemyDBManager, setup_db) -> requests.Session:
    app = create_app(test_app_db_manager, add_admin_app=test_settings.add_admin_app)
    return TestClient(app)
