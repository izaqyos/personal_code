"""Logging configuration for Repo Cleaner."""

import logging
import sys
from typing import Optional


def setup_logger(
    name: str = "repo_cleaner",
    level: int = logging.INFO,
    log_file: Optional[str] = None,
) -> logging.Logger:
    """Set up and return a configured logger.
    
    Args:
        name: Logger name
        level: Logging level (default: INFO)
        log_file: Optional path to log file
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Format based on level
    if level <= logging.DEBUG:
        fmt = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    else:
        fmt = "%(levelname)s: %(message)s"
    
    console_formatter = logging.Formatter(fmt)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler (if specified)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str = "repo_cleaner") -> logging.Logger:
    """Get an existing logger or create a default one.
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        return setup_logger(name)
    return logger


# Default logger instance
logger = get_logger()

