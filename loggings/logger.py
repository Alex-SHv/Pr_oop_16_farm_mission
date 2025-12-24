import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

DOCUMENTS_DIR = os.path.expanduser("~/Documents")
LOG_DIR = os.path.join(DOCUMENTS_DIR, "logs")  
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'farm_game.log' )

def get_logger(name="FARM_GAME"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    )

    handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=2_000_000,
        backupCount=5,
        encoding="utf-8"
    )
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger