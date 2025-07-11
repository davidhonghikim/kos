import logging
import sys
from datetime import datetime

logger = logging.getLogger("KLF")
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", "%H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)

def log(level: str, *args):
    message = " ".join(map(str, args))
    if level == "debug":
        logger.debug(message)
    elif level == "info":
        logger.info(message)
    elif level == "warn":
        logger.warning(message)
    elif level == "error":
        logger.error(message)
    else:
        logger.info(message) 