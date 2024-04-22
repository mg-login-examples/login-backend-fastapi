import asyncio
import json
import logging
from typing import Any

from fastapi import WebSocket
from pymongo.database import Database

from data.schemas.users.user import User
from group_chat import socket_message_handler as group_chat_socket_message_handler
from utils.pubsub.pubsub import PubSub
from utils.pubsub.subscriber import Subscriber

from .websocket_actions import WebSocketActions
from .websocket_payload import WebSocketPayload

logger = logging.getLogger(__name__)


async def handle_websocket_traffic(
    websocket: WebSocket,
    current_user: User,
    pubsub: PubSub,
    mongo_db: Database,
    pubsub_subscribers_async_tasks: list[asyncio.Task],
):
    logger.debug(f"Started websocket session for user '{current_user.email}'")
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
                mongo_db,
                channel_to_subscriber,
                pubsub_subscribers_async_tasks,
            )
    except Exception as e:
        if (
            str(e)
            == 'Expected ASGI message "websocket.receive" or "websocket.disconnect", but got \'websocket.close\''
        ):
            logger.error(
                "Ignore error. Caused by FastAPI ASGI & HTTPX WSGI differences"
            )
        else:
            logger.error(
                f"Error in handle_websocket_traffic for user {current_user.email}"
            )
            logger.error(e)
    await _handle_socket_connection_close(channel_to_subscriber, current_user)
    logger.debug(f"Ended websocket session for user '{current_user.email}'")


async def _handle_socket_connection_close(
    channel_to_subscriber: dict[str, Subscriber], current_user: User
):
    # When websocket connection is terminated, close all channel subscriptions
    # background tasks / infinite loops
    logger.debug(f"Closing all channel subscriptions for user f{current_user.email}")
    for channel in channel_to_subscriber:
        subscriber = channel_to_subscriber[channel]
        await subscriber.exit_async_iter()
        logger.debug(
            f"Closed channel '{channel}' subscription for user f{current_user.email}"
        )


async def _handle_websocket_incomming_message(
    socket_payload_json: dict,
    websocket: WebSocket,
    current_user: User,
    pubsub: PubSub,
    mongo_db: Database,
    channel_to_subscriber: dict[str, Subscriber],
    pubsub_subscribers_async_tasks: list[asyncio.Task],
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
                pubsub_subscribers_async_tasks,
            )
        # Action unsubscribe to channel
        if socket_payload.action == WebSocketActions.UNSUBSCRIBE.value:
            await _handle_action_unsubscribe_from_channel(
                socket_payload.channel,
                websocket,
                current_user,
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
                mongo_db,
                channel_to_subscriber,
            )
    except Exception as e:
        logger.error(
            f"Error while handling websocket message {socket_payload_json} for user {current_user.email}"
        )
        logger.error(e)


async def _handle_action_subscribe_to_channel(
    channel: str,
    websocket: WebSocket,
    current_user: User,
    pubsub: PubSub,
    channel_to_subscriber: dict,
    pubsub_subscribers_async_tasks: list[asyncio.Task],
):
    try:
        # TODO User permission check before subscribing
        if channel not in channel_to_subscriber:
            logger.debug(
                f"Creating subscriber async task for user {current_user.email} for channel '{channel}'"
            )
            subscriber_task = asyncio.create_task(
                _subscribe_to_channel(
                    channel,
                    websocket,
                    current_user,
                    pubsub,
                    channel_to_subscriber,
                )
            )
            # Collect task to gather during shutdown and ensure task is
            # completed for a graceful shutdown
            pubsub_subscribers_async_tasks.append(subscriber_task)
        else:
            logger.debug(
                f"Skipping creating subscriber task for user {current_user.email} for channel '{channel}'"
            )
        websocket_payload = {"channel": channel, "subscribed": True}
        await websocket.send_json(websocket_payload)
        logger.debug(
            f"Handled subscribe action to channel '{channel}' for user {current_user.email}"
        )
    except Exception as e:
        logger.error(
            f"Error in _handle_action_subscribe_to_channel for channel '{channel}' for user {current_user.email}"
        )
        logger.error(e)


async def _subscribe_to_channel(
    channel: str,
    websocket: WebSocket,
    current_user: User,
    pubsub: PubSub,
    channel_to_subscriber: dict,
):
    try:
        subscriber_name = f"user-{current_user.email}-channel-{channel}"
        async with pubsub.subscribe(
            channel=channel, subscriber_name=subscriber_name
        ) as subscriber:
            # since _subscribe_to_channel is an async task, check again if user already subscribed to channel (possibly by a parallel task), if so exit
            if channel in channel_to_subscriber:
                logger.debug(
                    f"Exiting subscriber's asynchronous context as user {current_user.email} is already subscribed to channel '{channel}'"
                )
                return
            # store subscriber to be able to later stop subscriber listen task
            channel_to_subscriber[channel] = subscriber
            logger.debug(
                f"Now inside subscriber's asynchronous context for user {current_user.email} and channel '{channel}'. Start listening to subscriber events"
            )
            # start listening to subscriber
            # indefinite async loop until subscriber.exit_async_iter is called externally from _handle_action_unsubscribe_from_channel
            async for event in subscriber:
                try:
                    # logger.debug(
                    #     f"Channel '{channel}' subscriber user '{current_user.email}' received event {event}"
                    # )
                    message_dict = json.loads(event.message)
                    websocket_payload = {"channel": channel, "message": message_dict}
                    await websocket.send_json(websocket_payload)
                except Exception as e:
                    logger.error(
                        f"Error in subscriber events'asynchronous iteration for user {current_user.email} for channel '{channel}':"
                    )
                    logger.error(e)
            logger.debug(
                f"Exited subscriber events' asynchronous iteration for user {current_user.email} and channel '{channel}'"
            )
        logger.debug(
            f"Exited subscriber's asynchronous context for user {current_user.email} and channel '{channel}'"
        )
    except Exception as e:
        logger.error(
            f"Error in subscriber's asynchronous context for user {current_user.email} for channel '{channel}':"
        )
        logger.error(e)


async def _handle_action_unsubscribe_from_channel(
    channel: str,
    websocket: WebSocket,
    current_user: User,
    channel_to_subscriber: dict[str, Subscriber],
):
    try:
        if channel in channel_to_subscriber:
            subscriber = channel_to_subscriber[channel]
            await subscriber.exit_async_iter()
            channel_to_subscriber.pop(channel)
        websocket_payload = {"channel": channel, "subscribed": False}
        await websocket.send_json(websocket_payload)
        logger.debug(f"User {current_user.email} unsubscribed from channel '{channel}'")
    except Exception as e:
        logger.error(
            f"Error in _handle_action_unsubscribe_from_channel for channel {channel} for user '{current_user.email}'"
        )
        logger.error(e)


async def _handle_channel_message(
    channel: str,
    message_data: Any,
    websocket: WebSocket,
    current_user: User,
    pubsub: PubSub,
    mongo_db: Database,
    channel_to_subscriber: dict,
):
    try:
        if channel in channel_to_subscriber:
            if channel.startswith("group-chat/"):
                await group_chat_socket_message_handler.handle_message(
                    channel,
                    message_data,
                    current_user,
                    pubsub,
                )
    except Exception as e:
        logger.error(
            f"Error in _handle_channel_message for channel {channel} for user '{current_user.email}'"
        )
        logger.error(e)
