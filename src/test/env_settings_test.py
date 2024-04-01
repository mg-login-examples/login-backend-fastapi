from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettingsTest(BaseSettings):
    admin_user_email: str = ""
    admin_user_password: str = ""
    playwright_app_base_url: str = "http://localhost:8018"
    model_config = SettingsConfigDict(env_prefix="test_")
