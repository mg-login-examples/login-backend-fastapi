import logging

from data.database.models.base import Base as BaseModel
from stores.sql_db_store.sql_alchemy_db_manager import SQLAlchemyDBManager

logger = logging.getLogger(__name__)


def create_all_tables(engine):
    BaseModel.metadata.create_all(bind=engine)
    logger.info("Created all db tables")
