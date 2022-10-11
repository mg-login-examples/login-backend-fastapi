import os
import sys
import logging
import asyncio

import uvicorn

from core.environment_settings import get_environment_settings
from core.logging_settings import set_logging_settings
from stores.store_utils import get_db_manager
from stores.store_utils import get_cache_manager
from stores.nosql_db_store import pymongo_manager
from core.app_factory import create_app
from stores.sql_db_store import db_utils
from core import admin_users_manager

logger = logging.getLogger(__name__)

# Init settings
dot_env_file = os.getenv("ENV_FILE", ".env")
SETTINGS = get_environment_settings(dot_env_file=dot_env_file)

# Set logging
set_logging_settings(SETTINGS.log_level, SETTINGS.log_to_file, SETTINGS.log_filename)
logger.info(f"Environment file selected: {dot_env_file}")

# Create db manager
app_db_manager = get_db_manager(SETTINGS.database_url, SETTINGS.database_user, SETTINGS.database_password)
# Create redis manager
redis_cache_manager = get_cache_manager(SETTINGS.redis_url, SETTINGS.redis_user, SETTINGS.redis_password)
# Create fastapi webapp
app = create_app(app_db_manager, redis_cache_manager, SETTINGS)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "create_db_tables":
            db_utils.create_all_tables(app_db_manager.engine)
        elif sys.argv[1] == "add_admin_user":
            admin_users_manager.create_admin_user(sys.argv[2], sys.argv[3], next(app_db_manager.db_session()))
        elif sys.argv[1] == "update_admin_user_password":
            admin_users_manager.update_admin_user_password(sys.argv[2], sys.argv[3], next(app_db_manager.db_session()))
        elif sys.argv[1] == "delete_admin_user":
            admin_users_manager.delete_admin_user(sys.argv[2], next(app_db_manager.db_session()))
        else:
            logger.error("Unknown argument received")
    else:
        # TODO Test db available
        if SETTINGS.test_redis_connection_on_app_start:
            asyncio.run(redis_cache_manager.assert_redis_is_available())
        if SETTINGS.test_pymongo_connection_on_app_start:
            pymongo_manager.assert_mongo_db_is_available(SETTINGS.mongo_host, SETTINGS.mongo_port)
        uvicorn.run(
            "main:app",
            host=SETTINGS.server_host,
            port=SETTINGS.server_port,
            log_config=None, # removes default uvicorn log level and formatting
            reload=True,
            workers=1
        )
