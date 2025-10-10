# app/utils.py
import logging
from pathlib import Path
from app.config import LOG_PATH

Path(LOG_PATH).parent.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=str(LOG_PATH),
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

def log_event(msg, level="info"):
    print(msg)
    if level == "debug":
        logging.debug(msg)
    elif level == "warning":
        logging.warning(msg)
    elif level == "error":
        logging.error(msg)
    else:
        logging.info(msg)
