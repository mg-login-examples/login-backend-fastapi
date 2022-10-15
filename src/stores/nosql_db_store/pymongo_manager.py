import logging

from pymongo import MongoClient
from pymongo.database import Database
from pymongo_inmemory import MongoClient as MongoClientInMemory

logger = logging.getLogger(__name__)

def get_db(
    mongo_host: str,
    mongo_port: int,
    mongo_username: str,
    mongo_password: str,
    mongo_database: str,
    use_in_memory_mongo_db: bool = False
) -> Database:
    if not use_in_memory_mongo_db:
        client = MongoClient(
            mongo_host,
            mongo_port,
            username=mongo_username,
            password=mongo_password,
        )
    else:
        client = MongoClientInMemory()
    db = client[mongo_database]
    return db

def assert_mongo_db_is_available(mongo_host: str, mongo_port: int, use_in_memory_mongo_db: bool = False):
    try:
        if not use_in_memory_mongo_db:
            client = MongoClient(mongo_host, mongo_port, serverSelectionTimeoutMS=1000)
        else:
            client = MongoClientInMemory()
        client.server_info()
        logger.info("Test mongo db connection established successfully")
    except Exception as e:
        logger.error("Error pinging to mongo")
        raise e
