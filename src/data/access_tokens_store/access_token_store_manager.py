import logging

from data.access_tokens_store.access_token_file_store import AccessTokenFileStore
from data.access_tokens_store.access_token_redis_store import AccessTokenRedisStore
from core.cache_manager import get_cache_manager

logger = logging.getLogger(__name__)

class AccessTokenStoreManager:

    def __init__(
        self,
        store_type = "in_memory_db",
        file_name: str = None,
        redis_url: str = None,
        redis_username: str = None,
        redis_password: str = None,
        redis_token_prefix: str = "",
    ):
        self.store_type = store_type
        if store_type == "file":
            self.file_store = AccessTokenFileStore(file_name)
        if store_type == "in_memory_db":
            self.app_redis_manager = get_cache_manager(redis_url, redis_username, redis_password)
            self.redis_token_prefix = redis_token_prefix
        logger.debug(f"access token store type: {self.store_type}")

    async def get_store(self):
        if self.store_type == "file":
            yield self.file_store
        if self.store_type == "in_memory_db":
            try:
                redis_session = self.app_redis_manager.redis_session()
                redis_store = AccessTokenRedisStore(redis_session, redis_token_prefix=self.redis_token_prefix)
                yield redis_store
            finally:
                await redis_session.close()
