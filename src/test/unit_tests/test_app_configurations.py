from settings.environment_settings import Settings
from data.database.sqlAlchemyDBManager import SQLAlchemyDBManager
import app_configurations

def test__app_settings():
    assert isinstance(app_configurations.app_settings, Settings)

def test__app_db_manager():
    assert isinstance(app_configurations.app_db_manager, SQLAlchemyDBManager)
