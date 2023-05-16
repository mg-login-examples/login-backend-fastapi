from pydantic import BaseSettings

class EnvSettingsTest(BaseSettings):
    admin_user_email: str = ''
    admin_user_password: str = ''
    playwright_app_base_url: str = 'http://localhost:8018'

    class Config:
        env_prefix = 'test_'
