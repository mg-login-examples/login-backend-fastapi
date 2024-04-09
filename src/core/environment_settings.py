import logging

import sec  # type: ignore

from core.helper_classes.settings import Settings

logger = logging.getLogger(__name__)


def get_environment_settings(dot_env_file: str = ".env"):
    settings = Settings(_env_file=dot_env_file)  # type: ignore

    docker_mysql_secret = sec.load("mysql-password")
    if docker_mysql_secret:
        settings.database_password = docker_mysql_secret

    docker_mongo_secret = sec.load("mongo-password")
    if docker_mongo_secret:
        settings.mongo_password = docker_mongo_secret

    redis_secret = sec.load("redis-pass")
    if redis_secret:
        settings.redis_password = redis_secret

    return settings
