
import logging
import json

from starlette.testclient import WebSocketTestSession
from broadcaster import Broadcast

from test.integration_tests.utils.async_testclient_for_websockets import AsyncioWebSocketTestSession

logger = logging.getLogger(__name__)

# Test that a group-chat channel can be subscribed to
def test_subscribe_to_group_chat(websocket_session: WebSocketTestSession):
    chat_room = "some_room"
    channel_name = f"group-chat/{chat_room}"
    websocket_session.send_json(data={"action": "subscribe", "channel": channel_name})
    subscribe_response = websocket_session.receive_json()
    assert subscribe_response["channel"] == channel_name
    assert subscribe_response["subscribed"] == True

# Test that a group-chat channel can be unsubscribed to
def test_unsubscribe_to_group_chat(websocket_session: WebSocketTestSession):
    chat_room = "some_room"
    channel_name = f"group-chat/{chat_room}"
    websocket_session.send_json(data={"action": "unsubscribe", "channel": channel_name})
    subscribe_response = websocket_session.receive_json()
    assert subscribe_response["channel"] == channel_name
    assert subscribe_response["subscribed"] == False

# Test that when subscribed to a group-chat, broadcasted messages in the group chat will be received
async def test_receive_group_chat_broadcast(app_broadcaster: Broadcast, async_websocket_session: AsyncioWebSocketTestSession):
        chat_room = "some_room"
        channel_name = f"group-chat/{chat_room}"
        await async_websocket_session.send_json(data={"action": "subscribe", "channel": channel_name})
        subscribe_response = await async_websocket_session.receive_json()
        assert subscribe_response["channel"] == channel_name
        assert subscribe_response["subscribed"] == True
        broadcast_to_channel_payload = {"user": "some_user", "text": "some text"}
        broadcast_to_channel_payload_str = json.dumps(broadcast_to_channel_payload)
        await app_broadcaster.publish(channel_name, broadcast_to_channel_payload_str)
        websocket_broadcast_response = await async_websocket_session.receive_json()
        assert websocket_broadcast_response["channel"] == channel_name
        assert websocket_broadcast_response["message"] == broadcast_to_channel_payload
