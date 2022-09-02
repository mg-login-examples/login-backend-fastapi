import pytest
import logging

from fastapi import FastAPI

from core.helper_classes.settings import Settings
from core.db_manager import get_db_manager
from core.helper_classes.sqlAlchemyDBManager import SQLAlchemyDBManager
from core.app_factory import create_app

logger = logging.getLogger(__name__)

@pytest.fixture
def app_db_manager(app_settings: Settings):
    app_db_manager = get_db_manager(app_settings.database_url, app_settings.database_user, app_settings.database_password)
    return app_db_manager

@pytest.fixture
def app(app_settings: Settings, app_db_manager: SQLAlchemyDBManager) -> FastAPI:
    app = create_app(app_db_manager, app_settings)
    return app
