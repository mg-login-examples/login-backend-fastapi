import logging

from fastapi.applications import FastAPI

from main import app

logger = logging.getLogger(__name__)

def test_app():
    logger.info("Testing app is instance of FastAPI")
    assert(isinstance(app, FastAPI))
