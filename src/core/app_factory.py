import logging

from fastapi import FastAPI
from broadcaster import Broadcast

from core.cors_settings import add_cors
from rest_endpoints import routes as api_routes
from socket_endpoints import routes as socket_routes
from admin_app import app_mounter as admin_app_mounter
from password_reset_app import app_mounter as password_reset_app_mounter
from core.helper_classes.settings import Settings
from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager
from stores.redis_store.aioredis_cache_manager import AioRedisCacheManager
from api_dependencies.dependencies_manager import get_user_routes_dependencies, get_admin_routes_dependencies, get_socket_route_dependencies
from utils.encode_broadcaster import broadcaster_utils as encode_broadcaster_utils
from core.swagger_docs import create_swagger_docs_for_user_endpoints, create_swagger_docs_for_admin_endpoints

logger = logging.getLogger(__name__)

def create_app(
    app_db_manager: SQLAlchemyDBManager,
    app_cache_manager: AioRedisCacheManager,
    broadcast: Broadcast,
    SETTINGS: Settings
) -> FastAPI:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

    api_routes_dependencies = get_user_routes_dependencies(
        app_db_manager,
        app_cache_manager,
        SETTINGS
    )
    admin_api_routes_dependencies = get_admin_routes_dependencies(
        app_db_manager,
        app_cache_manager,
        SETTINGS
    )
    api_router = api_routes.get_router(
        api_routes_dependencies,
        admin_api_routes_dependencies,
        SETTINGS.add_admin_app,
        SETTINGS.samesite,
        SETTINGS.secure_cookies,
    )
    app.include_router(api_router)

    if SETTINGS.add_websocket:
        socket_route_dependencies = get_socket_route_dependencies(
            app_db_manager,
            app_cache_manager,
            SETTINGS
        )
        broadcast_subscribers_async_tasks = []
        encode_broadcaster_utils.enable_broadcaster(app, broadcast, broadcast_subscribers_async_tasks)
        socket_router = socket_routes.get_router(
            broadcast,
            socket_route_dependencies,
            broadcast_subscribers_async_tasks,
        )
        app.include_router(socket_router)

    if SETTINGS.add_admin_app:
        admin_app_mounter.mount_app(app)
    if SETTINGS.add_password_reset_app:
        password_reset_app_mounter.mount_app(app)

    add_cors(app, SETTINGS.cors_origins_set)

    create_swagger_docs_for_user_endpoints(app, api_routes_dependencies, SETTINGS.samesite, SETTINGS.secure_cookies)
    create_swagger_docs_for_admin_endpoints(app, admin_api_routes_dependencies, SETTINGS.secure_cookies)

    return app
