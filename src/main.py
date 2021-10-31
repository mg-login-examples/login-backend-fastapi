from appFactory import create_app
from core.settings import settings
import uvicorn
import logging
import coloredlogs


coloredlogs.install(
    level=settings.log_level,
    fmt='%(asctime)s,%(msecs)03d %(name)s[%(process)d] %(levelname)s %(message)s'
)
logger = logging.getLogger(__name__)
logger.info(f"Log level set: {settings.log_level}")

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.server_host,
        port=settings.server_port,
        log_config=None,
        reload=True,
        workers=1
    )
