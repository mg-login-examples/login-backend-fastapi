from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager
from stores.nosql_db_store.pymongo_manager import PyMongoManager
from stores.redis_store.aioredis_cache_manager import AioRedisCacheManager

def get_db_manager(database_url: str, database_user: str, database_password: str) -> SQLAlchemyDBManager:
    db_manager = SQLAlchemyDBManager(
        database_url,
        database_user,
        database_password
    )
    return db_manager

def get_nosql_db_manager(
    mongo_host: str,
    mongo_port: int,
    mongo_username: str,
    mongo_password: str,
    mongo_database: str,
    use_in_memory_mongo_db: bool,
):
    nosql_db_manager = PyMongoManager(
        mongo_host,
        mongo_port,
        mongo_username,
        mongo_password,
        mongo_database,
        use_in_memory_mongo_db,
    )
    return nosql_db_manager

def get_cache_manager(redis_url: str, redis_user: str, redis_password: str) -> AioRedisCacheManager:
    cache_manager = AioRedisCacheManager(
        redis_url,
        redis_user,
        redis_password
    )
    return cache_manager
