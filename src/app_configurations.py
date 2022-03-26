import os
import logging

from settings.environment_settings import Settings
from settings.logger_settings import set_logger_settings
from data.database.sqlAlchemyDBManager import SQLAlchemyDBManager

logger = logging.getLogger(__name__)

ENV_FILE = os.getenv("ENV_FILE", ".env")
app_settings = Settings(_env_file=ENV_FILE)

set_logger_settings(app_settings.log_level)

logger.info(f".env file selected: {ENV_FILE}")

app_db_manager = SQLAlchemyDBManager(
    app_settings.database_url,
    app_settings.database_user,
    app_settings.database_password
)
