from typing import Literal
from pydantic import BaseSettings

class Settings(BaseSettings):
    server_port: int = 8000
    server_host: str = '0.0.0.0'
    log_level: str = "INFO"
    log_to_file: bool = True
    log_filename: str = "app.log"
    reload_app_on_change: bool = True

    database_url: str = 'sqlite:///./sql_app.db'
    database_user: str = ''
    database_password: str = ''
    test_sql_db_connection_on_app_start: bool = True

    mongo_host: str ='localhost'
    mongo_port: int = 27017
    mongo_username: str = ''
    mongo_password: str = ''
    mongo_database: str = 'login'
    use_in_memory_mongo_db: bool = True
    test_mongo_db_connection_on_app_start: bool = True

    access_tokens_store_type: Literal["file", "redis"] = 'file'
    redis_url: str = ''
    redis_user: str = ''
    redis_password: str = ''
    test_redis_connection_on_app_start: bool = False

    add_admin_app: bool = True
    add_password_reset_app: bool = True
    cors_origins_set: str = "Development"
    samesite: str = "lax"
    secure_cookies: bool = False

    add_websocket: bool = True
    broadcast_url: str = "memory://"
    test_broadcast_connection_on_app_start: bool = True
