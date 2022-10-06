import sec

from core.helper_classes.settings import Settings

def get_environment_settings(dot_env_file: str = ".env"):
    settings = Settings(_env_file=dot_env_file)

    docker_mysql_secret = sec.load("mysql-password")
    if docker_mysql_secret:
        settings.database_password = docker_mysql_secret

    docker_mongo_secret = sec.load("mongo-password")
    if docker_mongo_secret:
        settings.mongo_password = docker_mongo_secret

    return settings
