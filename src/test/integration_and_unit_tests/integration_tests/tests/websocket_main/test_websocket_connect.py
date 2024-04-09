import asyncio
import logging
import time

import pytest
from fastapi.exceptions import HTTPException
from fastapi.testclient import TestClient

from data.schemas.users.user import User

logger = logging.getLogger(__name__)

# Test that main websocket can be connected for a logged in user


# @pytest.mark.timeout(20)
# def test_socket_connect(
#     test_client_logged_in: TestClient,
#     logged_in_user: User,
#     test_client_after_app_start: TestClient,
#     app_pubsub,
# ):
#     pass


#     with test_client_after_app_start.websocket_connect("/ws/main") as websocket_session:
#         dummy_channel = "dummy_channel"
#         websocket_session.send_json(
#             data={"action": "subscribe", "channel": dummy_channel}
#         )
#         subscribe_response = websocket_session.receive_json()
#         assert subscribe_response["channel"] == dummy_channel
#         logger.info("************ 1")
#         time.sleep(5)
#         # asyncio.run(asyncio.sleep(5))
#         logger.info("************ 2")

#         # Wait for subscribe to channel background task to start
#     time.sleep(5)
#     logger.info("********** 3")
#     try:
#         asyncio.run(app_pubsub.disconnect())
#     except Exception as e:
#         logger.error(e)
#     # asyncio.run(asyncio.sleep(2))
#     time.sleep(5)
# logger.info("***********************************")


# # Test that main websocket cannot be connected if not logged in
# def test_socket_connect_fails_when_not_logged_in(test_client_after_app_start: TestClient):
#     try:
#         with test_client_after_app_start.websocket_connect("/ws/main") as websocket_session:
#             pass
#     except HTTPException as e:
#         assert e.status_code == 403
#         assert e.detail == "Not authenticated"
