from fastapi import Depends
from pymongo.database import Database

from stores.nosql_db_store.pymongo_manager import get_db as get_nosql_db

def get_nosql_db_as_fastapi_dependency(
    mongo_host: str,
    mongo_port: int,
    mongo_username: str,
    mongo_password: str,
    mongo_database: str,
):
    def get_db() -> Database:
        return get_nosql_db(mongo_host, mongo_port, mongo_username, mongo_password, mongo_database)

    return Depends(get_db)
