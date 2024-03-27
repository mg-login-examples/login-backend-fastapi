import logging

from fastapi.applications import FastAPI

from main import app

logger = logging.getLogger(__name__)


def test_app():
    assert (isinstance(app, FastAPI))
