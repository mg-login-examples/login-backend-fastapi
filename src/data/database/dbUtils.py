import logging

from data.database.models.base import Base as BaseModel

logger = logging.getLogger(__name__)

logger.info("Setting up SQL Alchemy")

def create_all_tables(engine):
    logger.info("Creating all tables")
    BaseModel.metadata.create_all(bind=engine)
