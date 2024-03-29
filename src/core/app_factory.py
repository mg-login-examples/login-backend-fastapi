import logging

from fastapi import FastAPI

from core.cors_settings import add_cors
from core.app_lifespan import get_lifespan
from rest_endpoints import routes as api_routes
from socket_endpoints import routes as socket_routes
from admin_app import app_mounter as admin_app_mounter
from password_reset_app import app_mounter as password_reset_app_mounter
from core.helper_classes.settings import Settings
from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager
from stores.nosql_db_store.pymongo_manager import PyMongoManager
from stores.redis_store.redis_cache_manager import RedisCacheManager
from api_dependencies.dependencies_manager import get_user_routes_dependencies, get_admin_routes_dependencies, get_socket_route_dependencies
from utils.pubsub.pubsub import PubSub

from core.swagger_docs import create_swagger_docs_for_user_endpoints, create_swagger_docs_for_admin_endpoints

logger = logging.getLogger(__name__)

def create_app(
    app_db_manager: SQLAlchemyDBManager,
    app_nosql_db_manager: PyMongoManager,
    app_cache_manager: RedisCacheManager,
    pubsub: PubSub,
    SETTINGS: Settings
) -> FastAPI:
    pubsub_subscribers_async_tasks = []

    app = FastAPI(lifespan=get_lifespan(pubsub, pubsub_subscribers_async_tasks), docs_url=None, redoc_url=None, openapi_url=None)

    api_routes_dependencies = get_user_routes_dependencies(
        app_db_manager,
        app_nosql_db_manager,
        app_cache_manager,
        pubsub,
        SETTINGS
    )
    admin_api_routes_dependencies = get_admin_routes_dependencies(
        app_db_manager,
        app_nosql_db_manager,
        app_cache_manager,
        pubsub,
        SETTINGS
    )
    api_router = api_routes.get_router(
        api_routes_dependencies,
        admin_api_routes_dependencies,
        SETTINGS.user_auth_cookie_type,
        SETTINGS.admin_user_auth_cookie_type,
        SETTINGS.add_admin_app,
    )
    app.include_router(api_router)

    if SETTINGS.add_websocket:
        socket_route_dependencies = get_socket_route_dependencies(
            app_db_manager,
            app_nosql_db_manager,
            app_cache_manager,
            pubsub,
            SETTINGS
        )
        socket_router = socket_routes.get_router(
            socket_route_dependencies,
            pubsub_subscribers_async_tasks,
        )
        app.include_router(socket_router)

    if SETTINGS.add_admin_app:
        admin_app_mounter.mount_app(app)
    if SETTINGS.add_password_reset_app:
        password_reset_app_mounter.mount_app(app)

    add_cors(app, SETTINGS.cors_origins_set)

    create_swagger_docs_for_user_endpoints(app, api_routes_dependencies, SETTINGS.user_auth_cookie_type)
    create_swagger_docs_for_admin_endpoints(app, admin_api_routes_dependencies, SETTINGS.admin_user_auth_cookie_type)

    return app
