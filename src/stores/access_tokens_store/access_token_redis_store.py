import logging

from aioredis import Redis

from utils.security.access_token_utils import parse_access_token
from stores.access_tokens_store.access_token_store import AccessTokenStore

logger = logging.getLogger(__name__)

class AccessTokenRedisStore(AccessTokenStore):
    def __init__(self, redis_session: Redis, redis_token_prefix = ""):
        self.redis_session = redis_session
        self.redis_token_prefix = redis_token_prefix

    async def check_if_access_token_is_valid(self, access_token: str):
        if (await super().check_if_access_token_is_valid(access_token)):
            user_id = parse_access_token(access_token, "user_id")
            user_id_key = f"{self.redis_token_prefix}-{user_id}"
            user_access_token = await self.redis_session.hget(user_id_key, access_token)
            if user_access_token:
                return True
        return False

    async def add_access_token(self, user_id: int, access_token: str):
        user_id_key = f"{self.redis_token_prefix}-{user_id}"
        await self.redis_session.hset(user_id_key, access_token, 1)

    async def remove_access_token(self, user_id: int, access_token: str):
        user_id_key = f"{self.redis_token_prefix}-{user_id}"
        await self.redis_session.hdel(user_id_key, access_token)
