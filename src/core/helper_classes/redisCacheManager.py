import logging

import aioredis

logger = logging.getLogger(__name__)

class RedisCacheManager():

    def __init__(self, redis_url: str, redis_user: str, redis_password: str):
        logger.debug("Setting up SQLAlchemy")

        self.redis_url = redis_url
        self.redis_user = redis_user
        self.redis_password = redis_password

    def redis_session(self):
        redis = aioredis.from_url(self.redis_url, username=self.redis_user, password=self.redis_password)
        return redis

    def redis_session_decode_string(self):
        redis = aioredis.from_url(self.redis_url, username=self.redis_user, password=self.redis_password, decode_responses=True)
        return redis
