import logging

from data.database.models.base import Base as BaseModel

logger = logging.getLogger(__name__)

def create_all_tables(engine):
    BaseModel.metadata.create_all(bind=engine)
    logger.info("Created all db tables")
