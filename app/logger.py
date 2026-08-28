import json
import logging
import os


LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "agent.log")


def setup_logger():
    """
    Configure debug logging for the Aster & Row agent.
    """

    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger("aster_row")
    logger.setLevel(logging.DEBUG)

    # Prevent duplicate log handlers during tests.
    if logger.handlers:
        return logger

    handler = logging.FileHandler(LOG_FILE)
    handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(message)s"
    )

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = setup_logger()


def log_event(event, **data):
    """
    Write a structured event to the debug log.

    Only sanitized information should be passed here.
    """

    payload = {
        "event": event,
        **data,
    }

    logger.info(
        json.dumps(
            payload,
            default=str
        )
    )
