from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    server_port: int = 8000
    server_host: str = "0.0.0.0"
    log_level: str = "INFO"
    log_to_file: bool = True
    log_filename: str = "../app.log"
    log_env_vars_on_app_start: bool = False
    reload_app_on_change: bool = True

    database_url: str = "sqlite:///./sql_app.db"
    database_user: str = ""
    database_password: str = ""
    check_sql_db_connection_on_app_start: bool = True

    mongo_host: str = "localhost"
    mongo_port: int = 27017
    mongo_username: str = ""
    mongo_password: str = ""
    mongo_database: str = "login"
    use_in_memory_mongo_db: bool = True
    check_mongo_db_connection_on_app_start: bool = True

    access_tokens_store_type: Literal["file", "redis"] = "file"
    redis_url: str = ""
    redis_password: str = ""
    check_redis_connection_on_app_start: bool = False

    add_admin_app: bool = True
    add_password_reset_app: bool = True

    cors_origins_set: Literal["Development", "Cloud-Development", "Production"] = (
        "Development"
    )
    user_auth_cookie_type: Literal[
        "cross_site_secure",
        "same_site_secure",
        "same_site_not_secure",
        "localhost_development",
    ] = "localhost_development"
    admin_user_auth_cookie_type: Literal[
        "cross_site_secure",
        "same_site_secure",
        "same_site_not_secure",
        "localhost_development",
    ] = "localhost_development"
    # cross_site_secure used for production when frontend & backend on different domains,
    # same_site_secure used for production when frontend & backend on same domain
    # samesite_not_secure used for docker e2e testing
    # localhost_development used for local development

    add_websocket: bool = True
    pubsub_url: str = "memory://"
    check_pubsub_connection_on_app_start: bool = True
