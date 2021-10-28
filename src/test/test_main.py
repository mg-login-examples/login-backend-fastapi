from fastapi.applications import FastAPI
import logging
from main import app

logger = logging.getLogger(__name__)
def test_app():
    logger.info("Testing app is instance of FastAPI")
    assert(isinstance(app, FastAPI))
