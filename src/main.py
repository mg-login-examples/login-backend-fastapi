import logging

import uvicorn
import coloredlogs

from configurations.settings import settings
from appFactory import create_app
from data.database.dbManager import db_manager
from data.database import dbUtils


coloredlogs.install(
    level=settings.log_level,
    fmt='%(asctime)s,%(msecs)03d %(name)s[%(process)d] %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)
logger.info(f"Log level set: {settings.log_level}")

app = create_app()

if __name__ == "__main__":
    dbUtils.create_all_tables(db_manager.engine)
    uvicorn.run(
        "main:app",
        host=settings.server_host,
        port=settings.server_port,
        log_config=None,
        reload=True,
        workers=1
    )
