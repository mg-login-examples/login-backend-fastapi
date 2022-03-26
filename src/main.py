import uvicorn

from app_configurations import app_settings
from app_factory import create_app
from app_configurations import app_db_manager
from data.database import dbUtils

app = create_app()

if __name__ == "__main__":
    dbUtils.create_all_tables(app_db_manager.engine)
    uvicorn.run(
        "main:app",
        host=app_settings.server_host,
        port=app_settings.server_port,
        log_config=None,
        reload=True,
        workers=1
    )
