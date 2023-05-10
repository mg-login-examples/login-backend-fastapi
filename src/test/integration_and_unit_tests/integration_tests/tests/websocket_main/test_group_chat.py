
import logging
import json
import pytest
import time

from starlette.testclient import WebSocketTestSession
# from test.integration_and_unit_tests.integration_tests.utils.async_testclient_for_websockets import AsyncioWebSocketTestSession
from httpx_ws import AsyncWebSocketSession

from utils.pubsub.pubsub import PubSub

logger = logging.getLogger(__name__)

# Test that a group-chat channel can be subscribed to
def test_subscribe_to_group_chat(websocket_session: WebSocketTestSession):
    chat_room = "some_room"
    channel_name = f"group-chat/{chat_room}"
    websocket_session.send_json(data={"action": "subscribe", "channel": channel_name})
    subscribe_response = websocket_session.receive_json()
    assert subscribe_response["channel"] == channel_name
    assert subscribe_response["subscribed"] == True
    time.sleep(0.1) # Wait for subscribe to channel background task to start

# Test that a group-chat channel can be unsubscribed to
def test_unsubscribe_to_group_chat(websocket_session: WebSocketTestSession):
    chat_room = "some_room"
    channel_name = f"group-chat/{chat_room}"
    websocket_session.send_json(data={"action": "subscribe", "channel": channel_name})
    subscribe_response = websocket_session.receive_json()
    assert subscribe_response["channel"] == channel_name
    assert subscribe_response["subscribed"] == True
    time.sleep(0.1) # Wait for subscribe to channel background task to start

    websocket_session.send_json(data={"action": "unsubscribe", "channel": channel_name})
    subscribe_response = websocket_session.receive_json()
    assert subscribe_response["channel"] == channel_name
    assert subscribe_response["subscribed"] == False
    time.sleep(0.1) # Wait for subscribe to channel background task to start

# Test that when subscribed to a group-chat, published messages in the group chat will be received
@pytest.mark.timeout(20)
async def test_receive_group_chat_from_pubsub(app_pubsub: PubSub, app_pubsub_connected: None, async_websocket_session: AsyncWebSocketSession):
    chat_room = "some_room"
    channel_name = f"group-chat/{chat_room}"
    await async_websocket_session.send_json(data={"action": "subscribe", "channel": channel_name})
    subscribe_response = await async_websocket_session.receive_json()
    assert subscribe_response["channel"] == channel_name
    assert subscribe_response["subscribed"] == True
    time.sleep(0.1) # Wait for subscribe to channel background task to start

    message_to_channel_payload = {"user": "some_user", "text": "some text"}
    message_to_channel_payload_str = json.dumps(message_to_channel_payload)
    await app_pubsub.publish(channel_name, message_to_channel_payload_str)
    websocket_response = await async_websocket_session.receive_json()
    assert websocket_response["channel"] == channel_name
    assert websocket_response["message"] == message_to_channel_payload
    time.sleep(0.1) # Wait for subscribe to channel background task to start
