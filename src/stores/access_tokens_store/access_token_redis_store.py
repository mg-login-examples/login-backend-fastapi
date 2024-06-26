import logging

from redis.asyncio.client import Redis

from stores.access_tokens_store.access_token_store import AccessTokenStore
from utils.redis import redis_utils
from utils.security.access_token_utils import parse_access_token

logger = logging.getLogger(__name__)


class AccessTokenRedisStore(AccessTokenStore):
    def __init__(self, redis_session: Redis, redis_token_prefix=""):
        self.redis_session = redis_session
        self.redis_token_prefix = redis_token_prefix

    async def check_if_access_token_is_valid(self, access_token: str):
        if await super().check_if_access_token_is_valid(access_token):
            user_id = parse_access_token(access_token, "user_id")
            user_id_key = f"{self.redis_token_prefix}-{user_id}"
            user_access_token: str | None = await redis_utils.redis_get(
                self.redis_session, user_id_key, access_token
            )
            if user_access_token:
                return True
        return False

    async def add_access_token(self, user_id: int, access_token: str):
        user_id_key = f"{self.redis_token_prefix}-{user_id}"
        await redis_utils.redis_add(self.redis_session, user_id_key, access_token, "1")

    async def remove_access_token(self, user_id: int, access_token: str):
        user_id_key = f"{self.redis_token_prefix}-{user_id}"
        await redis_utils.redis_remove(self.redis_session, user_id_key, access_token)
