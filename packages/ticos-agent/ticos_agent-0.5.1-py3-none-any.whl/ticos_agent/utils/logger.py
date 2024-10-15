import logging
from logging.handlers import RotatingFileHandler


def setup_logger(name, log_file=None, level=logging.INFO, max_size=10 * 1024 * 1024, backup_count=5):
    """Set up a logger with console and optionally file output.

    Args:
        name (str): Name of the logger.
        log_file (str, optional): Path to the log file. If None, only console logging is used.
        level (int, optional): Logging level. Defaults to logging.INFO.
        max_size (int, optional): Maximum size of the log file before it rotates. Defaults to 10MB.
        backup_count (int, optional): Number of backup log files to keep. Defaults to 5.

    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # Create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (if log_file is provided)
    if log_file:
        file_handler = RotatingFileHandler(log_file, maxBytes=max_size, backupCount=backup_count)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name):
    """Get or create a logger with the given name.

    This function returns an existing logger if one with the given name exists,
    otherwise it creates a new logger with default settings.

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Logger object.
    """
    return logging.getLogger(name)


# Default logger setup
default_logger = setup_logger("ticos_agent")
