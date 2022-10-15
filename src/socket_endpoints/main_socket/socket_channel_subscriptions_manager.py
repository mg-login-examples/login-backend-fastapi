from typing import Any, List
import logging
import asyncio
import json

from aiostream import stream
from broadcaster import Broadcast
from fastapi import WebSocket

from .websocket_payload import WebSocketPayload
from .subscribed_channels_stream_values import SubscribedChannelsStreamValues
from .websocket_actions import WebSocketActions
from helpers_classes.async_stream import AsyncStream
from data.schemas.users.user import User
from group_chat import socket_message_handler as group_chat_socket_message_handler

logger = logging.getLogger(__name__)

async def handle_websocket_traffic(
    websocket: WebSocket,
    current_user: User,
    broadcast: Broadcast,
    broadcast_subscribers_async_tasks: List[asyncio.Task]
):
    subscribed_channels_to_infinite_loop_handler_streams = {}
    # Subscribe to any global channels here
    #
    # End - Subscribe to any global channels here
    try:
        async for payload_json in websocket.iter_json():
            await _handle_websocket_incomming_message(
                payload_json,
                websocket,
                current_user,
                broadcast,
                subscribed_channels_to_infinite_loop_handler_streams,
                broadcast_subscribers_async_tasks
            )
    except Exception as e:
        logger.error("Error in handle_websocket_traffic")
        logger.error(e)
    await _handle_socket_connection_close(subscribed_channels_to_infinite_loop_handler_streams)

async def _handle_socket_connection_close(subscribed_channels_to_infinite_loop_handler_streams: dict):
    # When websocket connection is terminated, close all channel subscriptions background tasks / infinite loops
    for channel in subscribed_channels_to_infinite_loop_handler_streams:
        infinite_loop_handler = subscribed_channels_to_infinite_loop_handler_streams[channel]
        await infinite_loop_handler.put(SubscribedChannelsStreamValues.WEBSOCKET_CLOSED)

async def _handle_websocket_incomming_message(
    socket_payload_json: dict,
    websocket: WebSocket,
    current_user: User,
    broadcast: Broadcast,
    subscribed_channels_to_infinite_loop_handler_streams: dict,
    broadcast_subscribers_async_tasks: List[asyncio.Task]
    ):
    try:
        socket_payload = WebSocketPayload(**socket_payload_json)
        # Action subscribe to channel
        if socket_payload.action == WebSocketActions.SUBSCRIBE.value:
            await _handle_action_subscribe_to_channel(
                socket_payload.channel,
                websocket,
                current_user,
                broadcast,
                subscribed_channels_to_infinite_loop_handler_streams,
                broadcast_subscribers_async_tasks
            )
        # Action unsubscribe to channel
        if socket_payload.action == WebSocketActions.UNSUBSCRIBE.value:
            await _handle_action_unsubscribe_from_channel(
                socket_payload.channel,
                websocket,
                current_user,
                subscribed_channels_to_infinite_loop_handler_streams
            )
        # Action channel message
        if socket_payload.action == WebSocketActions.MESSAGE.value:
            await _handle_channel_message(
                socket_payload.channel,
                socket_payload.data,
                websocket,
                current_user,
                broadcast,
                subscribed_channels_to_infinite_loop_handler_streams,
            )
    except Exception as e:
        logger.error(f"Error while handling websocket message {socket_payload_json} for user {current_user.email}")
        logger.error(e)

async def _handle_action_subscribe_to_channel(
    channel: str,
    websocket: WebSocket,
    current_user: User,
    broadcast: Broadcast,
    subscribed_channels_to_infinite_loop_handler_streams: dict,
    broadcast_subscribers_async_tasks: List[asyncio.Task]
):
    # TODO User permission check before subscribing
    if channel not in subscribed_channels_to_infinite_loop_handler_streams:
        new_infinite_loop_handler_stream = AsyncStream()
        subscribed_channels_to_infinite_loop_handler_streams[channel] = new_infinite_loop_handler_stream
        subscriber_task = asyncio.create_task(
            _subscribe_to_channel(
                channel,
                websocket,
                broadcast,
                new_infinite_loop_handler_stream
            )
        )
        # Collect task to gather during shutdown and ensure task is completed for a graceful shutdown
        broadcast_subscribers_async_tasks.append(subscriber_task)
    websocket_payload = { "channel": channel, "message":{ "channelSubscribed": True } }
    await websocket.send_json(websocket_payload)

async def _subscribe_to_channel(
    channel: str,
    websocket: WebSocket,
    broadcast: Broadcast,
    new_infinite_loop_handler_stream: AsyncStream
):
    try:
        async with broadcast.subscribe(channel=channel) as subscriber:
            subscriber_and_my_stream = stream.merge(subscriber, new_infinite_loop_handler_stream)
            async with subscriber_and_my_stream.stream() as subscriber_and_my_stream_events:
                async for event in subscriber_and_my_stream_events:
                    if (
                        event == SubscribedChannelsStreamValues.CHANNEL_UNSUBSCRIBED or
                        event == SubscribedChannelsStreamValues.WEBSOCKET_CLOSED
                    ):
                        break
                    else:
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
    current_user: User,
    subscribed_channels_to_infinite_loop_handler_streams: dict,
):
    if channel in subscribed_channels_to_infinite_loop_handler_streams:
        infinite_loop_handler = subscribed_channels_to_infinite_loop_handler_streams[channel]
        await infinite_loop_handler.put(SubscribedChannelsStreamValues.CHANNEL_UNSUBSCRIBED)
        subscribed_channels_to_infinite_loop_handler_streams.pop(channel)
    websocket_payload = { "channel": channel, "message":{ "channelSubscribed": False } }
    await websocket.send_json(websocket_payload)

async def _handle_channel_message(
    channel: str,
    message_data: Any,
    websocket: WebSocket,
    current_user: User,
    broadcast: Broadcast,
    subscribed_channels_to_infinite_loop_handler_streams: dict,
):
    if channel in subscribed_channels_to_infinite_loop_handler_streams:
        if channel.startswith("group-chat/"):
            await group_chat_socket_message_handler.handle_message(
                channel,
                message_data,
                current_user,
                broadcast,
            )
