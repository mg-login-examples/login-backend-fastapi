import logging

from fastapi import Depends
from redis.asyncio.client import Redis

from stores.access_tokens_store.access_token_file_store import AccessTokenFileStore
from stores.access_tokens_store.access_token_redis_store import AccessTokenRedisStore

logger = logging.getLogger(__name__)


def get_access_token_store_as_fastapi_dependency(
    store_type="redis",
    redis_session_as_fastapi_dependency: Redis | None = None,
    redis_token_prefix: str = "",
    file_name: str | None = None,
):
    if store_type == "redis":

        def get_redis_based_token_store(
            redis_session: Redis | None = redis_session_as_fastapi_dependency,
        ):
            if not redis_session:
                raise Exception("Unexpected error. Redis is None!")
            redis_store = AccessTokenRedisStore(
                redis_session, redis_token_prefix=redis_token_prefix
            )
            return redis_store

        return Depends(get_redis_based_token_store)
    elif store_type == "file":
        if file_name is None:
            raise Exception("Filename cannot be none is store_type is file")

        def get_file_based_token_store():
            file_store = AccessTokenFileStore(file_name)
            return file_store

        return Depends(get_file_based_token_store)

    raise Exception(f'Unexpected store_type provided "{store_type}"')
