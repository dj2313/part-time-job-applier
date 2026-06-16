import logging
from logging.handlers import RotatingFileHandler
from config import LOG_DIR
import sys

def setup_logger():
    # Create a custom logger
    logger = logging.getLogger("minijob_agent")
    logger.setLevel(logging.INFO)

    # Prevent duplicating logs if the logger is already setup
    if logger.handlers:
        return logger

    # Create handlers
    console_handler = logging.StreamHandler(sys.stdout)
    file_handler = RotatingFileHandler(
        filename=LOG_DIR / "agent.log", 
        maxBytes=5 * 1024 * 1024, # 5 MB
        backupCount=3,
        encoding="utf-8"
    )

    # Create formatters and add it to handlers
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(log_format)
    file_handler.setFormatter(log_format)

    # Add handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger

# Create a global logger instance
logger = setup_logger()
