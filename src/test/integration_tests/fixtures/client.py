import pytest
import logging

import requests
from fastapi.testclient import TestClient

from app_factory import create_app
from test.integration_tests.fixtures.dbutils import setup_db

logger = logging.getLogger(__name__)

@pytest.fixture
def test_client(setup_db) -> requests.Session:
    return TestClient(create_app())
