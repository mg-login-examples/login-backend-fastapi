import os
import sys
import logging
import asyncio

import uvicorn

from core import (
    environment_settings,
    logging_settings,
    app_factory,
    admin_users_manager,
)
from stores import store_utils
from stores.sql_db_store import db_utils
from utils.pubsub import utils as pubsub_utils
from utils.pubsub.pubsub import PubSub

logger = logging.getLogger(__name__)

# Init settings
dot_env_file = os.getenv("ENV_FILE", ".env")
SETTINGS = environment_settings.get_environment_settings(dot_env_file=dot_env_file)

# Set logging
logging_settings.set_logging_settings(
    SETTINGS.log_level, SETTINGS.log_to_file, SETTINGS.log_filename
)
logger.info(f"Environment file selected: {dot_env_file}")
logging_settings.filter_out_healthcheck_logs()

# Create db manager
app_db_manager = store_utils.get_db_manager(
    SETTINGS.database_url, SETTINGS.database_user, SETTINGS.database_password
)
# Create nosql db manager
app_nosql_db_manager = store_utils.get_nosql_db_manager(
    SETTINGS.mongo_host,
    SETTINGS.mongo_port,
    SETTINGS.mongo_username,
    SETTINGS.mongo_password,
    SETTINGS.mongo_database,
    SETTINGS.use_in_memory_mongo_db,
)
# Create redis manager
redis_cache_manager = store_utils.get_cache_manager(
    SETTINGS.redis_url, SETTINGS.redis_password
)
# Create pubsub
pubsub = pubsub_utils.get_pubsub(SETTINGS.pubsub_url, SETTINGS.redis_password)
# Create fastapi webapp
app = app_factory.create_app(
    app_db_manager, app_nosql_db_manager, redis_cache_manager, pubsub, SETTINGS
)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "create_db_tables":
            db_utils.create_all_tables(app_db_manager.engine)
        elif sys.argv[1] == "add_admin_user":
            admin_users_manager.create_admin_user(
                sys.argv[2], sys.argv[3], next(app_db_manager.db_session())
            )
        elif sys.argv[1] == "update_admin_user_password":
            admin_users_manager.update_admin_user_password(
                sys.argv[2], sys.argv[3], next(app_db_manager.db_session())
            )
        elif sys.argv[1] == "delete_admin_user":
            admin_users_manager.delete_admin_user(
                sys.argv[2], next(app_db_manager.db_session())
            )
        else:
            logger.error("Unknown argument received")
    else:
        if SETTINGS.check_sql_db_connection_on_app_start:
            app_db_manager.assert_sql_db_is_available()
        if SETTINGS.check_redis_connection_on_app_start:
            asyncio.run(redis_cache_manager.assert_redis_is_available())
        if SETTINGS.check_mongo_db_connection_on_app_start:
            app_nosql_db_manager.assert_mongo_db_is_available()
        if SETTINGS.check_pubsub_connection_on_app_start:
            asyncio.run(
                pubsub_utils.assert_pubsub_is_able_to_connect_to_backend(pubsub)
            )
        uvicorn.run(
            "main:app",
            host=SETTINGS.server_host,
            port=SETTINGS.server_port,
            log_config=None,  # removes default uvicorn log level and formatting
            reload=SETTINGS.reload_app_on_change,
            workers=1,
        )
