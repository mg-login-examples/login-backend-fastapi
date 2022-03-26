import logging

import coloredlogs

logger = logging.getLogger(__name__)

def set_logger_settings(log_level):
    coloredlogs.install(
        level=log_level,
        fmt='%(asctime)s,%(msecs)03d %(name)s[%(process)d] %(levelname)s %(message)s'
    )
    logger.info(f"Log level set: {log_level}")
