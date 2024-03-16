import sec
import logging

from core.helper_classes.settings import Settings

logger = logging.getLogger(__name__)

def get_environment_settings(dot_env_file: str = ".env"):
    settings = Settings(_env_file=dot_env_file)

    docker_mysql_secret = sec.load("mysql-password")
    if docker_mysql_secret:
        settings.database_password = docker_mysql_secret

    docker_mongo_secret = sec.load("mongo-password")
    if docker_mongo_secret:
        settings.mongo_password = docker_mongo_secret

    redis_secret = sec.load("redis-pass")
    if redis_secret:
        settings.redis_password = redis_secret

    if settings.log_env_vars_on_app_start:
        logger.info("****************** ENV Vars ******************")
        settings_dict = settings.model_dump()
        for setting in settings_dict:
            logger.info(f'{setting}={settings_dict[setting]}')
        logger.info("**********************************************")

    return settings
