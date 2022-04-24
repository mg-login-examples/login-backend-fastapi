import os
import sec

from core.helper_classes.settings import Settings

def get_environment_settings(dot_env_file: str = ".env"):
    docker_mysql_secret = sec.load("mysql-password")
    if docker_mysql_secret:
        settings = Settings(_env_file=dot_env_file, database_password=docker_mysql_secret)
    else:
        settings = Settings(_env_file=dot_env_file)
    return settings
