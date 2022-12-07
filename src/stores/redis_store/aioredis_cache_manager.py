import logging

import aioredis

logger = logging.getLogger(__name__)

class AioRedisCacheManager():

    def __init__(self, redis_url: str, redis_password: str):
        logger.debug("Setting up SQLAlchemy")

        self.redis_url = redis_url
        self.redis_password = redis_password

    async def redis_session(self):
        try:
            redis = aioredis.from_url(
                self.redis_url,
                password=self.redis_password,
                decode_responses=True
            )
            yield redis
        finally:
            await redis.close()

    async def assert_redis_is_available(self):
        try:
            redis = aioredis.from_url(
                self.redis_url,
                password=self.redis_password,
                socket_connect_timeout=1
            )
            await redis.ping()
            logger.info("Test redis connection established successfully")
        except Exception as e:
            logger.error("Error pinging to Redis")
            raise e
