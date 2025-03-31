import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime, timedelta

from app.config import LOG_DIR, LOG_FILE, LOG_MAX_SIZE, LOG_RETENTION_DAYS

# Ensure the logs directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Setup Rotating File Handler
log_handler = RotatingFileHandler(
    LOG_FILE, maxBytes=LOG_MAX_SIZE, backupCount=5  # Rotate and keep 5 old logs
)

log_formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
)
log_handler.setFormatter(log_formatter)

logger = logging.getLogger("fcm_logger")
logger.setLevel(logging.INFO)
logger.addHandler(log_handler)

# Function to delete old logs
def cleanup_old_logs():
    now = datetime.now()
    for filename in os.listdir(LOG_DIR):
        file_path = os.path.join(LOG_DIR, filename)
        if filename.startswith("fcm_server.log"):
            file_time = datetime.fromtimestamp(os.path.getctime(file_path))
            if now - file_time > timedelta(days=LOG_RETENTION_DAYS):
                os.remove(file_path)
                logger.info(f"Deleted old log: {filename}")

# Run cleanup when the server starts
cleanup_old_logs()

# Example log entry
logger.info("Logging system initialized")
