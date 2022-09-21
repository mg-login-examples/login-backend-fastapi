from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager
from stores.redis_store.aioredis_cache_manager import AioRedisCacheManager

def get_db_manager(database_url: str, database_user: str, database_password: str) -> SQLAlchemyDBManager:
    db_manager = SQLAlchemyDBManager(
        database_url,
        database_user,
        database_password
    )
    return db_manager

def get_cache_manager(redis_url: str, redis_user: str, redis_password: str) -> AioRedisCacheManager:
    cache_manager = AioRedisCacheManager(
        redis_url,
        redis_user,
        redis_password
    )
    return cache_manager
