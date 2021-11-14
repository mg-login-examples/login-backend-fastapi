import pytest
import logging

import requests
from fastapi.testclient import TestClient

from app_factory import create_app
from app_configurations import app_db_manager
from test.integration_tests.fixtures.dbutils import setup_db

logger = logging.getLogger(__name__)

@pytest.fixture
def test_client(setup_db) -> requests.Session:
    app = create_app()
    return TestClient(app)
