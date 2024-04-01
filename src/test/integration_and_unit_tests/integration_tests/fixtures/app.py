import logging

import pytest
from fastapi import FastAPI

from core import app_factory
from core.helper_classes.settings import Settings
from stores.nosql_db_store.pymongo_manager import PyMongoManager
from stores.redis_store.redis_cache_manager import RedisCacheManager
from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager
from stores.store_utils import (get_cache_manager, get_db_manager,
                                get_nosql_db_manager)
from utils.pubsub import utils as pubsub_utils
from utils.pubsub.pubsub import PubSub

logger = logging.getLogger(__name__)


@pytest.fixture
def app_db_manager(app_settings: Settings):
    logger.debug("Create fixture app_db_manager")
    app_db_manager = get_db_manager(
        app_settings.database_url,
        app_settings.database_user,
        app_settings.database_password,
    )
    return app_db_manager


@pytest.fixture
def app_nosql_db_manager(app_settings: Settings):
    logger.debug("Create fixture app_nosql_db_manager")
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
    logger.debug("Create fixture app_cache_manager")
    app_cache_manager = get_cache_manager(
        app_settings.redis_url, app_settings.redis_password
    )
    return app_cache_manager


@pytest.fixture
def app_pubsub(app_settings: Settings):
    logger.debug("Create fixture app_pubsub")
    return pubsub_utils.get_pubsub(
        pubsub_url=app_settings.pubsub_url, redis_pass=app_settings.redis_password
    )


@pytest.fixture
async def app_pubsub_connected(app_pubsub: PubSub):
    logger.debug("Create fixture app_pubsub_connected")
    await app_pubsub.connect()


@pytest.fixture
def app(
    app_settings: Settings,
    app_db_manager: SQLAlchemyDBManager,
    app_nosql_db_manager: PyMongoManager,
    app_cache_manager: RedisCacheManager,
    app_pubsub: PubSub,
) -> FastAPI:
    logger.debug("Create fixture app")
    app = app_factory.create_app(
        app_db_manager,
        app_nosql_db_manager,
        app_cache_manager,
        app_pubsub,
        app_settings,
    )
    return app
