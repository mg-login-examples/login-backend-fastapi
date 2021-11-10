import logging

from fastapi.applications import FastAPI

from main import app
from test.integration_tests.fixtures.dbutils import setup_db

logger = logging.getLogger(__name__)

def test_app():
    logger.info("Testing app is instance of FastAPI")
    assert(isinstance(app, FastAPI))
