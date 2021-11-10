import pytest
import logging

from app_configurations import app_db_manager
from data.database import dbUtils

logger = logging.getLogger(__name__)

@pytest.fixture
def setup_db():
    dbUtils.create_all_tables(app_db_manager.engine)
