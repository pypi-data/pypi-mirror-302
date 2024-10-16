# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Configure logging for the Environment Manager.

"""
import logging
from pathlib import Path


def get_handler(log_file_path: Path) -> logging.StreamHandler:
    """Return a logging handler for the Environment Manager."""
    try:
        if log_file_path.parent.is_dir():
            return logging.FileHandler(str(log_file_path))
        return logging.StreamHandler()
    except Exception:
        pass

    return logging.StreamHandler()


def get_logger(name: str | None = None) -> logging.Logger:
    """Configure custom logger for the Environment Manager."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    log_file = Path("/opt") / ".qbraid" / "lem.log"
    handler = get_handler(log_file)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
