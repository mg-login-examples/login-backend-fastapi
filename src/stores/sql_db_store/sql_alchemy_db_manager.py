import logging
from sqlite3 import Connection as SQLite3Connection

from sqlalchemy import create_engine, pool, event
from sqlalchemy.engine import make_url, URL, Engine
from sqlalchemy.orm import sessionmaker


logger = logging.getLogger(__name__)


class SQLAlchemyDBManager():

    def __init__(self, database_url: str, database_user: str,
                 database_password: str):
        logger.debug("Setting up SQLAlchemy")
        self.database_url = database_url
        self.database_user = database_user
        self.database_password = database_password

        self.sqlalchemy_url = SQLAlchemyDBManager.generate_sqlalchemy_url(
            database_url,
            database_user=database_user,
            database_password=database_password,
        )

        if "sqlite" in database_url:
            self.enable_sqlite_foreign_keys()
            self.engine = create_engine(
                self.sqlalchemy_url, connect_args={"check_same_thread": False}
            )
        else:
            self.engine = create_engine(self.sqlalchemy_url)

        self.Session = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine)

    def db_session(self):
        session = self.Session()
        try:
            yield session
        finally:
            session.close()

    @staticmethod
    def generate_sqlalchemy_url(
            database_url: str, database_user: str, database_password: str) -> URL:
        sqlalchemy_url = make_url(database_url)

        if not "sqlite" in database_url:
            if not sqlalchemy_url.username:
                sqlalchemy_url = sqlalchemy_url.set(username=database_user)
            if not sqlalchemy_url.password:
                sqlalchemy_url = sqlalchemy_url.set(password=database_password)

        return sqlalchemy_url

    @staticmethod
    def create_sqlalchemy_engine_for_alembic(
            database_url: str, database_user: str, database_password: str):
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

    def assert_sql_db_is_available(self):
        try:
            sqlalchemy_url = SQLAlchemyDBManager.generate_sqlalchemy_url(
                self.database_url,
                database_user=self.database_user,
                database_password=self.database_password,
            )

            engine = None
            if "sqlite" in self.database_url:
                engine = create_engine(
                    sqlalchemy_url,
                    poolclass=pool.NullPool,
                    connect_args={"check_same_thread": False},
                    pool_pre_ping=True
                )
            else:
                engine = create_engine(
                    sqlalchemy_url,
                    poolclass=pool.NullPool,
                    pool_pre_ping=True
                )
            with engine.connect() as connection:
                pass
            logger.info("Test sql db connection established successfully")
        except Exception as e:
            logger.error("Error pinging to mysql")
            raise e

    def enable_sqlite_foreign_keys(self):
        # https://stackoverflow.com/questions/5033547/sqlalchemy-cascade-delete/62327279#62327279
        @event.listens_for(Engine, "connect")
        def _set_sqlite_pragma(dbapi_connection, connection_record):
            if isinstance(dbapi_connection, SQLite3Connection):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON;")
                cursor.close()
