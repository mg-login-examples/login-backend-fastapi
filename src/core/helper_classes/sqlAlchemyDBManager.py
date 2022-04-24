import logging

from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

class SQLAlchemyDBManager():

    def __init__(self, database_url: str, database_user: str, database_password: str):
        logger.info("Setting up SQLAlchemy")

        if "sqlite" in database_url:
            self.URL_CONFIG = make_url(database_url)
            self.engine = create_engine(
                self.URL_CONFIG, connect_args={"check_same_thread": False}
            )
        else:
            self.URL_CONFIG = make_url(database_url)
            if not self.URL_CONFIG.username:
                self.URL_CONFIG = self.URL_CONFIG.set(username=database_user)
            if not self.URL_CONFIG.password:
                self.URL_CONFIG = self.URL_CONFIG.set(password=database_password)
            self.engine = create_engine(self.URL_CONFIG)

        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def db_session(self):
        session = self.Session()
        try:
            yield session
        finally:
            session.close()
