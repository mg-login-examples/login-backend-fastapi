import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

class SQLAlchemyDBManager():

    def __init__(self, database_url: str, database_user: str, database_password: str):
        logger.info("Setting up SQLAlchemy")

        if "sqlite" in database_url:
            self.SQLALCHEMY_DATABASE_URL = database_url
            self.engine = create_engine(
                self.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
            )
        else:
            self.SQLALCHEMY_DATABASE_URL = database_url
            self.engine = create_engine(self.SQLALCHEMY_DATABASE_URL)

        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def db_session(self):
        session = self.Session()
        try:
            yield session
        finally:
            session.close()
