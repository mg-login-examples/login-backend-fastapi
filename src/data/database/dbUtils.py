import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configurations.settings import settings
from data.database.models import base

logger = logging.getLogger(__name__)

logger.info("Setting up SQL Alchemy")

def create_all_tables(engine):
    logger.info("Creating all tables")
    base.Base.metadata.create_all(bind=engine)
