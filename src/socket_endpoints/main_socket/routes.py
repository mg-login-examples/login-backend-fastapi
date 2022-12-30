from typing import List
import asyncio

from fastapi import WebSocket

from helpers_classes.custom_api_router import APIRouter
from api_dependencies.common_route_dependencies import CommonRouteDependencies
from data.schemas.users.user import User
from socket_endpoints.main_socket.socket_channel_subscriptions_manager import handle_websocket_traffic
from utils.pubsub.pubsub import PubSub

def get_router(
    api_routes_dependencies: CommonRouteDependencies,
    pubsub_subscribers_async_tasks: List[asyncio.Task]
) -> APIRouter:

    router = APIRouter()

    @router.websocket("/main")
    async def ws_main(websocket: WebSocket, current_user: User = api_routes_dependencies.current_user, pubsub: PubSub = api_routes_dependencies.pubsub):
        await websocket.accept()

        await handle_websocket_traffic(websocket, current_user, pubsub, pubsub_subscribers_async_tasks)

    return router
