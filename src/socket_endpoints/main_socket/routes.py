import asyncio

from fastapi import WebSocket
from pymongo.database import Database

from api_dependencies.socket_route_dependencies import SocketRouteDependencies
from data.schemas.users.user import User
from helpers_classes.custom_api_router import APIRouter
from socket_endpoints.main_socket.socket_channel_subscriptions_manager import (
    handle_websocket_traffic,
)
from utils.pubsub.pubsub import PubSub


def get_router(
    socket_route_dependencies: SocketRouteDependencies,
    pubsub_subscribers_async_tasks: list[asyncio.Task],
) -> APIRouter:

    router = APIRouter()

    @router.websocket("/main")
    async def ws_main(
        websocket: WebSocket,
        current_user: User = socket_route_dependencies.current_user,
        pubsub: PubSub = socket_route_dependencies.pubsub,
        mongo_db: Database = socket_route_dependencies.mongo_db,
    ):
        await websocket.accept()

        await handle_websocket_traffic(
            websocket, current_user, pubsub, mongo_db, pubsub_subscribers_async_tasks
        )

    return router
