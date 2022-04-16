# import pytest
# from unittest.mock import MagicMock, patch
# from typing import Generator

# from data.database.sqlAlchemyDBManager import SQLAlchemyDBManager

# @patch("data.database.sqlAlchemyDBManager.sessionmaker")
# @patch("data.database.sqlAlchemyDBManager.create_engine")
# def test__SQLAlchemyDBManager__init__with__sqlite_url(
#     mock_create_engine: MagicMock,
#     mock_sessionmaker: MagicMock
# ):
#     mock_engine = MagicMock()
#     mock_create_engine.return_value = mock_engine
#     mock_Session = MagicMock()
#     mock_sessionmaker.return_value = mock_Session
#     test_database_url = "sqlite:///./sql_app.db"

#     db_manager = SQLAlchemyDBManager(test_database_url, None, None)

#     assert db_manager.SQLALCHEMY_DATABASE_URL == test_database_url
#     mock_create_engine.assert_called_with(
#         test_database_url,
#         connect_args={"check_same_thread": False}
#     )
#     db_manager.engine = mock_engine

#     mock_sessionmaker.assert_called_once_with(autocommit=False, autoflush=False, bind=mock_engine)
#     db_manager.Session = mock_Session

# @patch("data.database.sqlAlchemyDBManager.sessionmaker")
# @patch("data.database.sqlAlchemyDBManager.create_engine")
# def test__SQLAlchemyDBManager__init__with__postgresql_url(
#     mock_create_engine: MagicMock,
#     mock_sessionmaker: MagicMock
# ):
#     mock_engine = MagicMock()
#     mock_create_engine.return_value = mock_engine
#     mock_Session = MagicMock()
#     mock_sessionmaker.return_value = mock_Session
#     test_database_url = "postgresql://user:password@postgresserver/db"

#     db_manager = SQLAlchemyDBManager(test_database_url, None, None)

#     assert db_manager.SQLALCHEMY_DATABASE_URL == test_database_url
#     mock_create_engine.assert_called_with(test_database_url)
#     db_manager.engine = mock_engine

#     mock_sessionmaker.assert_called_once_with(autocommit=False, autoflush=False, bind=mock_engine)
#     db_manager.Session = mock_Session


# @patch("data.database.sqlAlchemyDBManager.sessionmaker")
# @patch("data.database.sqlAlchemyDBManager.create_engine")
# def test__SQLAlchemyDBManager__db_session(
#     mock_create_engine: MagicMock,
#     mock_sessionmaker: MagicMock
# ):
#     mock_db_session = MagicMock()
#     mock_Session = MagicMock(return_value=mock_db_session)
#     mock_sessionmaker.return_value = mock_Session
#     test_database_url = "test_url"
#     db_manager = SQLAlchemyDBManager(test_database_url, None, None)

#     db_generator = db_manager.db_session()
#     mock_Session.assert_not_called()
#     assert isinstance(db_generator, Generator) 

#     db = db_generator.__next__()
#     assert db == mock_db_session
#     mock_Session.assert_called_once()

#     mock_db_session.close.assert_not_called()
#     with pytest.raises(StopIteration):
#         db_generator.__next__()
#     mock_db_session.close.assert_called()
    
