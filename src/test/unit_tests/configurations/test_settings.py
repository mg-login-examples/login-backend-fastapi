from pydantic import BaseSettings
from settings.environment_settings import Settings

def test__settings():
    assert issubclass(Settings, BaseSettings)
