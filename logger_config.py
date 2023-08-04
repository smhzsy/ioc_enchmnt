import logging
import os

from dotenv import load_dotenv

load_dotenv()

OUTPUT_LOG_FILE = os.getenv("OUTPUT_LOG_PATH")
ERROR_LOG_FILE = os.getenv("ERROR_LOG_PATH")

LOG_LEVEL = logging.INFO
ERROR_LOG_LEVEL = logging.ERROR

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


def configure_logging():
    logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, filename=OUTPUT_LOG_FILE)

    error_logger = logging.getLogger('error_logger')
    error_handler = logging.FileHandler(ERROR_LOG_FILE)
    error_handler.setLevel(ERROR_LOG_LEVEL)
    error_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    error_logger.addHandler(error_handler)


def get_logger():
    return logging.getLogger('main_logger')


def get_error_logger():
    error_logger = logging.getLogger('error_logger')
    return error_logger
