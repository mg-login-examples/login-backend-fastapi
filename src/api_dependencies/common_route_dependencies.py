from typing import Any

from sqlalchemy.orm import Session
from redis.asyncio.client import Redis
from pymongo.database import Database as NoSQLDatabase

from stores.access_tokens_store.access_token_store import AccessTokenStore
from data.schemas.users.user import User
from utils.pubsub.pubsub import PubSub


class CommonRouteDependencies:
    def __init__(
        self,
        db_session_as_dependency: Session,
        nosql_database_as_dependency: NoSQLDatabase,
        pubsub_as_dependency: PubSub,
        current_user_as_dependency: User,
        cache_session_as_dependency: Redis | None = None,
        access_token_store_as_dependency: AccessTokenStore | None = None,
        validated_access_token_as_dependency: str | None = None,
        restrict_endpoint_to_own_resources_param_item_id_as_dependency: (
            Any | None
        ) = None,
        restrict_endpoint_to_own_resources_param_user_id_as_dependency: (
            Any | None
        ) = None,
    ):
        self.db = db_session_as_dependency
        self.nosql_database = nosql_database_as_dependency
        self.redis_cache_session = cache_session_as_dependency
        self.access_token_store = access_token_store_as_dependency
        self.pubsub = pubsub_as_dependency
        self.validated_access_token = validated_access_token_as_dependency
        self.current_user = current_user_as_dependency
        self.restrict_endpoint_to_own_resources_param_item_id = (
            restrict_endpoint_to_own_resources_param_item_id_as_dependency
        )
        self.restrict_endpoint_to_own_resources_param_user_id = (
            restrict_endpoint_to_own_resources_param_user_id_as_dependency
        )
