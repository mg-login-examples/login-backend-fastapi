import pytest
import logging

from data.database.dbManager import db_manager
from data.database import dbUtils

logger = logging.getLogger(__name__)

@pytest.fixture
def setup_db():
    dbUtils.create_all_tables(db_manager.engine)
