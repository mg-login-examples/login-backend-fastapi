import asyncio

from api_dependencies.socket_route_dependencies import SocketRouteDependencies
from helpers_classes.custom_api_router import APIRouter
from socket_endpoints.main_socket import routes as main_socket_routes


def get_router(
    socket_route_dependencies: SocketRouteDependencies,
    pubsub_subscribers_async_tasks: list[asyncio.Task],
) -> APIRouter:
    api_router = APIRouter(prefix="/ws")

    main_socket_router = main_socket_routes.get_router(
        socket_route_dependencies, pubsub_subscribers_async_tasks
    )
    api_router.include_router(main_socket_router)

    return api_router
