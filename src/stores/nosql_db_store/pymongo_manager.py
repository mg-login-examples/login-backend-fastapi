import logging

from pymongo import MongoClient
from pymongo.database import Database

logger = logging.getLogger(__name__)

def get_db(
    mongo_host: str,
    mongo_port: int,
    mongo_username: str,
    mongo_password: str,
    mongo_database: str,
) -> Database:
    client = MongoClient(
        mongo_host,
        mongo_port,
        username=mongo_username,
        password=mongo_password,
    )
    db = client[mongo_database]
    return db

def assert_mongo_db_is_available(mongo_host: str, mongo_port: int):
    try:
        client = MongoClient(mongo_host, mongo_port, serverSelectionTimeoutMS=1000)
        client.server_info()
        logger.info("Test mongo connection established successfully")
    except Exception as e:
        logger.error("Error pinging to mongo")
        raise e
