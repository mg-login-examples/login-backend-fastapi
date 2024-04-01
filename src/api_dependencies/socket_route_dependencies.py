from typing import Any

from sqlalchemy.orm import Session
from redis.asyncio.client import Redis
from pymongo.database import Database as NoSQLDatabase
from fastapi import Depends

from core.helper_classes.settings import Settings
from data.schemas.users.user import User
from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager
from stores.nosql_db_store.pymongo_manager import PyMongoManager
from stores.redis_store.redis_cache_manager import RedisCacheManager
from utils.pubsub.pubsub import PubSub
from stores.access_tokens_store.access_token_store import AccessTokenStore
from api_dependencies.dependencies.access_token_store import (
    get_access_token_store_as_fastapi_dependency,
)
from api_dependencies.dependencies.socket_authorization_token_extractor import (
    get_socket_authorization_token_as_fastapi_dependency,
)
from api_dependencies.dependencies.socket_validated_access_token import (
    get_socket_validated_access_token_as_fastapi_dependency,
)
from api_dependencies.dependencies.current_user import (
    get_current_user_as_fastapi_dependency,
)
from api_dependencies.dependencies.restrict_endpoint_to_own_resources_param_item_id_dependency import (
    get_restrict_endpoint_to_own_resources_param_item_id_as_fastapi_dependency,
)
from api_dependencies.dependencies.restrict_endpoint_to_own_resources_param_user_id_dependency import (
    get_restrict_endpoint_to_own_resources_param_user_id_as_fastapi_dependency,
)


class SocketRouteDependencies:
    def __init__(
        self,
        db_session_as_dependency: Session,
        mongo_database_as_dependency: NoSQLDatabase,
        redis_cache_session_as_dependency: Redis,
        pubsub_as_dependency: PubSub,
        access_token_store_as_dependency: AccessTokenStore,
        validated_access_token_as_dependency: str,
        current_user_as_dependency: User,
        restrict_endpoint_to_own_resources_param_item_id_as_dependency: Any,
        restrict_endpoint_to_own_resources_param_user_id_as_dependency: Any,
    ):
        self.sql_db_session = db_session_as_dependency
        self.mongo_db = mongo_database_as_dependency
        self.redis_cache_session = redis_cache_session_as_dependency
        self.pubsub = pubsub_as_dependency
        self.access_token_store = access_token_store_as_dependency
        self.validated_access_token = validated_access_token_as_dependency
        self.current_user = current_user_as_dependency
        self.restrict_endpoint_to_own_resources_param_item_id = (
            restrict_endpoint_to_own_resources_param_item_id_as_dependency
        )
        self.restrict_endpoint_to_own_resources_param_user_id = (
            restrict_endpoint_to_own_resources_param_user_id_as_dependency
        )


def get_socket_routes_dependencies(
    app_db_manager: SQLAlchemyDBManager,
    app_mongo_db_manager: PyMongoManager,
    app_cache_manager: RedisCacheManager,
    pubsub: PubSub,
    settings: Settings,
):
    db_session_as_dependency = Depends(app_db_manager.db_session)
    mongo_database_as_dependency = Depends(app_mongo_db_manager.get_db)
    redis_cache_session_as_dependency = Depends(app_cache_manager.redis_session)
    token_extractor_as_dependency = (
        get_socket_authorization_token_as_fastapi_dependency()
    )
    access_token_store_as_dependency = get_access_token_store_as_fastapi_dependency(
        store_type=settings.access_tokens_store_type,
        redis_session_as_fastapi_dependency=redis_cache_session_as_dependency,
        redis_token_prefix="user",
        file_name="user_access_tokens.txt",
    )
    validated_access_token_as_dependency = (
        get_socket_validated_access_token_as_fastapi_dependency(
            token_extractor_as_dependency, access_token_store_as_dependency
        )
    )
    current_user_as_dependency = get_current_user_as_fastapi_dependency(
        validated_access_token_as_dependency, db_session_as_dependency
    )
    restrict_endpoint_to_own_resources_param_item_id_as_dependency = (
        get_restrict_endpoint_to_own_resources_param_item_id_as_fastapi_dependency(
            current_user_as_dependency
        )
    )
    restrict_endpoint_to_own_resources_param_user_id_as_dependency = (
        get_restrict_endpoint_to_own_resources_param_user_id_as_fastapi_dependency(
            current_user_as_dependency
        )
    )

    return SocketRouteDependencies(
        db_session_as_dependency=db_session_as_dependency,
        mongo_database_as_dependency=mongo_database_as_dependency,
        redis_cache_session_as_dependency=redis_cache_session_as_dependency,
        pubsub_as_dependency=pubsub.get_pubsub_as_fastapi_dependency(),
        access_token_store_as_dependency=access_token_store_as_dependency,
        validated_access_token_as_dependency=validated_access_token_as_dependency,
        current_user_as_dependency=current_user_as_dependency,
        restrict_endpoint_to_own_resources_param_item_id_as_dependency=restrict_endpoint_to_own_resources_param_item_id_as_dependency,
        restrict_endpoint_to_own_resources_param_user_id_as_dependency=restrict_endpoint_to_own_resources_param_user_id_as_dependency,
    )
