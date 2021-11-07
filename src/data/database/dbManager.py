import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from configurations.settings import settings

logger = logging.getLogger(__name__)



class SQLAlchemyDBManager():

    def __init__(self):
        logger.info("Setting up SQLAlchemy")

        if "sqlite" in settings.database_url:
            self.SQLALCHEMY_DATABASE_URL = settings.database_url
            self.engine = create_engine(
                self.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
            )
        else:
            self.SQLALCHEMY_DATABASE_URL = settings.database_url
            self.engine = create_engine(self.SQLALCHEMY_DATABASE_URL)

        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def get_db_session(self):
        db = self.Session()
        try:
            yield db
        finally:
            db.close()


db_manager = SQLAlchemyDBManager()