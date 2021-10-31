import os
import logging
from pydantic import BaseSettings

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    server_port: int = 8000
    server_host: str = '0.0.0.0'
    log_level: str = "INFO"

    database_url: str = ''
    database_user: str = ''
    database_password: str = ''


ENV_FILE = os.getenv("ENV_FILE", ".env")
settings = Settings(_env_file=ENV_FILE)
