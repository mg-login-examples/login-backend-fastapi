import os

from settings.environment_settings import Settings
from data.database.sqlAlchemyDBManager import SQLAlchemyDBManager

ENV_FILE = os.getenv("ENV_FILE", ".env")
app_settings = Settings(_env_file=ENV_FILE)

app_db_manager = SQLAlchemyDBManager(
    app_settings.database_url,
    app_settings.database_user,
    app_settings.database_password
)
