from typing import List
import asyncio

from broadcaster import Broadcast

from socket_endpoints.main_socket import routes as main_socket_routes
from helpers_classes.custom_api_router import APIRouter
from api_dependencies.common_route_dependencies import CommonRouteDependencies

def get_router(
    broadcast: Broadcast,
    api_routes_dependencies: CommonRouteDependencies,
    broadcast_subscribers_async_tasks: List[asyncio.Task],
) -> APIRouter:
    api_router = APIRouter(prefix="/ws")

    main_socket_router = main_socket_routes.get_router(broadcast, api_routes_dependencies, broadcast_subscribers_async_tasks)
    api_router.include_router(main_socket_router)

    return api_router    
