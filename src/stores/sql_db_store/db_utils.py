import logging

from data.database.models.base import Base as BaseModel
from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager

logger = logging.getLogger(__name__)

def create_all_tables(engine):
    BaseModel.metadata.create_all(bind=engine)
    logger.info("Created all db tables")

def assert_sql_db_is_available(database_url: str, database_user: str, database_password: str):
    try:
        SQLAlchemyDBManager.ping_database(database_url, database_user, database_password)
        logger.info("Test sql db connection established successfully")
    except Exception as e:
        logger.error("Error pinging to mysql")
        raise e
