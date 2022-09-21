from typing import Literal
from pydantic import BaseSettings

class Settings(BaseSettings):
    server_port: int = 8000
    server_host: str = '0.0.0.0'
    log_level: str = "INFO"
    log_to_file: bool = True
    log_filename: str = "app.log"

    database_url: str = ''
    database_user: str = ''
    database_password: str = ''

    access_tokens_store_type: Literal["file", "in_memory_db"] = 'file'
    redis_url: str = ''
    redis_user: str = ''
    redis_password: str = ''
    test_redis_connection_on_app_start: bool = False

    add_admin_app: bool = True
    add_password_reset_app: bool = True
    cors_origins_set: str = "Development"
    samesite: str = "lax"
    secure_cookies: bool = False
