import os
import logging

import uvicorn

from core.settings import Settings
from core.logging_settings import set_logging_settings
from core.db_manager import get_db_manager
from app_factory import create_app
from data.database import dbUtils

logger = logging.getLogger(__name__)

# Init settings
ENV_FILE = os.getenv("ENV_FILE", ".env")
SETTINGS = Settings(_env_file=ENV_FILE)

# Set logging
set_logging_settings(SETTINGS.log_level)
logger.info(f".env file selected: {ENV_FILE}")

# Create db manager
app_db_manager = get_db_manager(SETTINGS.database_url, SETTINGS.database_user, SETTINGS.database_password)
# Create fastapi webapp
app = create_app(app_db_manager, SETTINGS.add_admin_app)

if __name__ == "__main__":
    dbUtils.create_all_tables(app_db_manager.engine)
    uvicorn.run(
        "main:app",
        host=SETTINGS.server_host,
        port=SETTINGS.server_port,
        log_config=None, # removes default uvicorn log level and formatting
        reload=True,
        workers=1
    )
