from typing import Any, List
import logging
import asyncio
import json

from fastapi import WebSocket

from .websocket_payload import WebSocketPayload
from .websocket_actions import WebSocketActions
from data.schemas.users.user import User
from group_chat import socket_message_handler as group_chat_socket_message_handler
from utils.pubsub.pubsub import PubSub
from utils.pubsub.subscriber import Subscriber

logger = logging.getLogger(__name__)

async def handle_websocket_traffic(
    websocket: WebSocket,
    current_user: User,
    pubsub: PubSub,
    pubsub_subscribers_async_tasks: List[asyncio.Task]
):
    channel_to_subscriber: dict[str, Subscriber] = {}
    # Subscribe to any global channels here
    #
    # End - Subscribe to any global channels here
    try:
        async for payload_json in websocket.iter_json():
            await _handle_websocket_incomming_message(
                payload_json,
                websocket,
                current_user,
                pubsub,
                channel_to_subscriber,
                pubsub_subscribers_async_tasks
            )
    except Exception as e:
        logger.error("Error in handle_websocket_traffic")
        logger.error(e)
    await _handle_socket_connection_close(channel_to_subscriber)

async def _handle_socket_connection_close(channel_to_subscriber: dict[str, Subscriber]):
    # When websocket connection is terminated, close all channel subscriptions background tasks / infinite loops
    for channel in channel_to_subscriber:
        subscriber = channel_to_subscriber[channel]
        await subscriber.exit_async_iter()

async def _handle_websocket_incomming_message(
    socket_payload_json: dict,
    websocket: WebSocket,
    current_user: User,
    pubsub: PubSub,
    channel_to_subscriber: dict[str, Subscriber],
    pubsub_subscribers_async_tasks: List[asyncio.Task]
    ):
    try:
        socket_payload = WebSocketPayload(**socket_payload_json)
        # Action subscribe to channel
        if socket_payload.action == WebSocketActions.SUBSCRIBE.value:
            await _handle_action_subscribe_to_channel(
                socket_payload.channel,
                websocket,
                current_user,
                pubsub,
                channel_to_subscriber,
                pubsub_subscribers_async_tasks
            )
        # Action unsubscribe to channel
        if socket_payload.action == WebSocketActions.UNSUBSCRIBE.value:
            await _handle_action_unsubscribe_from_channel(
                socket_payload.channel,
                websocket,
                channel_to_subscriber,
            )
        # Action channel message
        if socket_payload.action == WebSocketActions.MESSAGE.value:
            await _handle_channel_message(
                socket_payload.channel,
                socket_payload.data,
                websocket,
                current_user,
                pubsub,
                channel_to_subscriber,
            )
    except Exception as e:
        logger.error(f"Error while handling websocket message {socket_payload_json} for user {current_user.email}")
        logger.error(e)

async def _handle_action_subscribe_to_channel(
    channel: str,
    websocket: WebSocket,
    current_user: User,
    pubsub: PubSub,
    channel_to_subscriber: dict,
    pubsub_subscribers_async_tasks: List[asyncio.Task]
):
    # TODO User permission check before subscribing
    if channel not in pubsub_subscribers_async_tasks:
        subscriber_task = asyncio.create_task(
            _subscribe_to_channel(
                channel,
                websocket,
                pubsub,
                channel_to_subscriber,
            )
        )
        # Collect task to gather during shutdown and ensure task is completed for a graceful shutdown
        pubsub_subscribers_async_tasks.append(subscriber_task)
    websocket_payload = { "channel": channel, "subscribed": True }
    await websocket.send_json(websocket_payload)

async def _subscribe_to_channel(
    channel: str,
    websocket: WebSocket,
    pubsub: PubSub,
    channel_to_subscriber: dict,
):
    try:
        async with pubsub.subscribe(channel=channel) as subscriber:
            # subscriber_and_my_stream = stream.merge(subscriber, new_infinite_loop_handler_stream)
            # async with subscriber_and_my_stream.stream() as subscriber_and_my_stream_events:
            if channel in channel_to_subscriber: 
                # highly unlikely case where a separate subscribe channel message from websocket is received
                # but subscriber not created and added to channel_to_subscriber thread when line 108 is executed in current thread
                return
            channel_to_subscriber[channel] = subscriber # store subscriber to be able to externally stop subscriber listen task
            async for event in subscriber:
                try:
                    message_dict = json.loads(event.message)
                    websocket_payload = { "channel": channel, "message": message_dict }
                    await websocket.send_json(websocket_payload)
                except Exception as e:
                    logger.error("Error in _subscribe_to_channel stream for channel {channel}")
                    logger.error(e)
    except Exception as e:
        logger.error(f"Error in _subscribe_to_channel for channel {channel}")
        logger.error(e)

async def _handle_action_unsubscribe_from_channel(
    channel: str,
    websocket: WebSocket,
    channel_to_subscriber: dict[str, Subscriber],
):
    if channel in channel_to_subscriber:
        subscriber = channel_to_subscriber[channel]
        await subscriber.exit_async_iter()
        channel_to_subscriber.pop(channel)
    websocket_payload = { "channel": channel, "subscribed": False }
    await websocket.send_json(websocket_payload)

async def _handle_channel_message(
    channel: str,
    message_data: Any,
    websocket: WebSocket,
    current_user: User,
    pubsub: PubSub,
    channel_to_subscriber: dict,
):
    if channel in channel_to_subscriber:
        if channel.startswith("group-chat/"):
            await group_chat_socket_message_handler.handle_message(
                channel,
                message_data,
                current_user,
                pubsub,
            )
