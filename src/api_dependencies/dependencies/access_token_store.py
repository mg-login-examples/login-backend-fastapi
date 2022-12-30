import logging

from redis.asyncio.client import Redis
from fastapi import Depends

from stores.access_tokens_store.access_token_file_store import AccessTokenFileStore
from stores.access_tokens_store.access_token_redis_store import AccessTokenRedisStore

logger = logging.getLogger(__name__)

def get_access_token_store_as_fastapi_dependency(
    store_type = "redis",
    redis_session_as_fastapi_dependency: Redis = None,
    redis_token_prefix: str = "",
    file_name: str = None,
):
    if store_type == "redis":
        def get_access_token_store(
            redis_session: Redis = redis_session_as_fastapi_dependency
        ):
            redis_store = AccessTokenRedisStore(redis_session, redis_token_prefix=redis_token_prefix)
            return redis_store
        return Depends(get_access_token_store)
    else:
        def get_access_token_store():
            file_store = AccessTokenFileStore(file_name)
            return file_store
        return Depends(get_access_token_store)
