import pytest
import logging
import os

import requests
from fastapi.testclient import TestClient

from core.settings import Settings
from core.db_manager import get_db_manager
from data.database.sqlAlchemyDBManager import SQLAlchemyDBManager
from data.database import dbUtils
from app_factory import create_app

logger = logging.getLogger(__name__)

@pytest.fixture
def test_settings() -> Settings:
    ENV_FILE = os.getenv("ENV_FILE", ".env")
    SETTINGS = Settings(_env_file=ENV_FILE)
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
