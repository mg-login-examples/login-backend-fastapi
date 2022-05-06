import logging

import coloredlogs

logger = logging.getLogger(__name__)

def set_logging_settings(log_level: str, log_to_file: bool, log_filename: str):
    if log_to_file:
        logging.basicConfig(filename=log_filename, encoding='utf-8')
    coloredlogs.install(
        level=log_level,
        fmt='%(asctime)s,%(msecs)03d %(name)s[%(process)d] %(levelname)s %(message)s'
    )
    logger.info(f"Log level set: {log_level}")
