import logging

import coloredlogs

logger = logging.getLogger(__name__)

def set_logging_settings(log_level: str, log_to_file: bool, log_filename: str):
    if log_to_file:
        file_format='%(asctime)s %(name)s[%(process)d] %(levelname)s %(message)s'
        logging.basicConfig(filename=log_filename, encoding='utf-8', format=file_format)
    coloredlogs_format='%(asctime)s,%(msecs)03d %(name)s[%(process)d] %(levelname)s %(message)s'
    coloredlogs.install(
        level=log_level,
        fmt=coloredlogs_format
    )
    logger.info(f"Log level set: {log_level}")
