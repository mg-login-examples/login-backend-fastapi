import os
import logging
from pydantic import BaseSettings

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    database_url: str = ''
    database_user: str = ''
    database_password: str = ''

    class Config:
        env_file = '.env'

ENV_FILE = os.getenv("ENV_FILE", ".env")
settings = Settings(_env_file=ENV_FILE)
