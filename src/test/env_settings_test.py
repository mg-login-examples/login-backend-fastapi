from pydantic import BaseSettings

class EnvSettingsTest(BaseSettings):
    admin_user_email: str = ''
    admin_user_password: str = ''

    class Config:
        env_prefix = 'test_'
