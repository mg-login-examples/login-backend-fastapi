import logging

from env_settings.settings import Settings
from utils.security import docker_secret_utils

logger = logging.getLogger(__name__)


def get_environment_settings(dot_env_file: str = ".env"):
    settings = Settings(_env_file=dot_env_file)  # type: ignore

    docker_mysql_secret = docker_secret_utils.load_from_run_secrets("mysql_pwd")
    if docker_mysql_secret:
        settings.database_password = docker_mysql_secret

    docker_mongo_secret = docker_secret_utils.load_from_run_secrets("mongo_pwd")
    if docker_mongo_secret:
        settings.mongo_password = docker_mongo_secret

    redis_secret = docker_secret_utils.load_from_run_secrets("redis_pwd")
    if redis_secret:
        settings.redis_password = redis_secret

    return settings
