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

    add_admin_app: bool = True
    cors_origins_set: str = "Development"
