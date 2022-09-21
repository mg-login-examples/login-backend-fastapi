import pytest
import logging

from fastapi import FastAPI

from core.helper_classes.settings import Settings
from stores.store_utils import get_db_manager, get_cache_manager
from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager
from stores.redis_store.aioredis_cache_manager import AioRedisCacheManager
from core.app_factory import create_app

logger = logging.getLogger(__name__)

@pytest.fixture
def app_db_manager(app_settings: Settings):
    app_db_manager = get_db_manager(app_settings.database_url, app_settings.database_user, app_settings.database_password)
    return app_db_manager

@pytest.fixture
def app_cache_manager(app_settings: Settings):
    app_db_manager = get_cache_manager(app_settings.redis_url, app_settings.redis_user, app_settings.redis_password)
    return app_db_manager

@pytest.fixture
def app(app_settings: Settings, app_db_manager: SQLAlchemyDBManager, app_cache_manager: AioRedisCacheManager) -> FastAPI:
    app = create_app(app_db_manager, app_cache_manager, app_settings)
    return app
