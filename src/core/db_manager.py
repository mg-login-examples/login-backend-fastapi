from data.database.sqlAlchemyDBManager import SQLAlchemyDBManager

def get_db_manager(database_url: str, database_user: str, database_password: str) -> SQLAlchemyDBManager:
    app_db_manager = SQLAlchemyDBManager(
        database_url,
        database_user,
        database_password
    )
    return app_db_manager
