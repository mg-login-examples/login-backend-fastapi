import logging
import pytest

from fastapi.testclient import TestClient
from starlette.testclient import WebSocketTestSession

logger = logging.getLogger(__name__)


@pytest.fixture
def websocket_session(test_client_logged_in: TestClient,
                      test_client_after_app_start: TestClient) -> WebSocketTestSession:
    logger.debug("Create fixture websocket_session")
    with test_client_after_app_start.websocket_connect("/ws/main") as websocket_session:
        yield websocket_session
