import pytest
import logging

from fastapi import FastAPI
from broadcaster import Broadcast

from core.helper_classes.settings import Settings
from stores.store_utils import get_db_manager, get_nosql_db_manager, get_cache_manager
from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager
from stores.nosql_db_store.pymongo_manager import PyMongoManager
from stores.redis_store.aioredis_cache_manager import AioRedisCacheManager
from core import app_factory
from utils.encode_broadcaster import broadcaster_utils as encode_broadcaster_utils

logger = logging.getLogger(__name__)

@pytest.fixture
def app_db_manager(app_settings: Settings):
    app_db_manager = get_db_manager(
        app_settings.database_url,
        app_settings.database_user,
        app_settings.database_password
    )
    return app_db_manager

@pytest.fixture
def app_nosql_db_manager(app_settings: Settings):
    app_nosql_db_manager = get_nosql_db_manager(
        app_settings.mongo_host,
        app_settings.mongo_port,
        app_settings.mongo_username,
        app_settings.mongo_password,
        app_settings.mongo_database,
        app_settings.use_in_memory_mongo_db,
    )
    return app_nosql_db_manager

@pytest.fixture
def app_cache_manager(app_settings: Settings):
    app_cache_manager = get_cache_manager(
        app_settings.redis_url,
        app_settings.redis_password
    )
    return app_cache_manager

@pytest.fixture
def app_broadcaster(app_settings: Settings):
    return encode_broadcaster_utils.get_broadcaster(app_settings.broadcast_url, redis_pass=app_settings.redis_password)

@pytest.fixture
def app(
    app_settings: Settings,
    app_db_manager: SQLAlchemyDBManager,
    app_nosql_db_manager: PyMongoManager,
    app_cache_manager: AioRedisCacheManager,
    app_broadcaster: Broadcast
) -> FastAPI:
    app = app_factory.create_app(
        app_db_manager,
        app_nosql_db_manager,
        app_cache_manager,
        app_broadcaster,
        app_settings
    )
    return app
