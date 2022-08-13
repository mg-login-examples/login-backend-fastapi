import logging

from sqlalchemy import create_engine, pool
from sqlalchemy.engine import make_url, URL
from sqlalchemy.orm import sessionmaker


logger = logging.getLogger(__name__)

class SQLAlchemyDBManager():

    def __init__(self, database_url: str, database_user: str, database_password: str):
        logger.debug("Setting up SQLAlchemy")

        self.sqlalchemy_url = SQLAlchemyDBManager.generate_sqlalchemy_url(
            database_url,
            database_user=database_user,
            database_password=database_password,
        )

        if "sqlite" in database_url:
            self.engine = create_engine(
                self.sqlalchemy_url, connect_args={"check_same_thread": False}
            )
        else:
            self.engine = create_engine(self.sqlalchemy_url)

        self.Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def db_session(self):
        session = self.Session()
        try:
            yield session
        finally:
            session.close()

    @staticmethod
    def generate_sqlalchemy_url(database_url: str, database_user: str, database_password: str) -> URL:
        sqlalchemy_url = make_url(database_url)

        if not "sqlite" in database_url:
            if not sqlalchemy_url.username:
                sqlalchemy_url = sqlalchemy_url.set(username=database_user)
            if not sqlalchemy_url.password:
                sqlalchemy_url = sqlalchemy_url.set(password=database_password)

        return sqlalchemy_url

    @staticmethod
    def create_sqlalchemy_engine_for_alembic(database_url: str, database_user: str, database_password: str):
        sqlalchemy_url = SQLAlchemyDBManager.generate_sqlalchemy_url(
            database_url,
            database_user=database_user,
            database_password=database_password,
        )

        if "sqlite" in database_url:
            return create_engine(
                sqlalchemy_url, 
                poolclass=pool.NullPool,
                connect_args={"check_same_thread": False}
            )
        else:
            return create_engine(
                sqlalchemy_url, 
                poolclass=pool.NullPool,
            )
