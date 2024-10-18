import logging
import os
from logging.handlers import RotatingFileHandler

from senren.config import get_config


def setup_logging():
    """Set up logging for the Senren project."""
    config = get_config()
    log_level = getattr(logging, config.LOG_LEVEL.upper())

    # Create logs directory if it doesn't exist
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Set up root logger
    logging.basicConfig(level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Set up file handler
    file_handler = RotatingFileHandler("logs/senren.log", maxBytes=10 * 1024 * 1024, backupCount=5)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))

    # Add file handler to root logger
    logging.getLogger("").addHandler(file_handler)

    # Set up loggers for each module
    logger_names = [
        "senren.cli",
        "senren.entity",
        "senren.data_source",
        "senren.feature_view",
        "senren.feature_service",
        "senren.online_store",
        "senren.repo",
    ]

    for name in logger_names:
        logger = logging.getLogger(name)
        logger.setLevel(log_level)
        logger.addHandler(file_handler)

    logging.info("Logging setup complete")


def get_logger(name: str) -> logging.Logger:
    """Get a logger for a specific module."""
    return logging.getLogger(name)
