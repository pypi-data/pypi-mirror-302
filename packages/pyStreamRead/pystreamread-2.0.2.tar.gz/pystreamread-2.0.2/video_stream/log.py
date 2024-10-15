import sys
import logging
import logging.config
import traceback

from logging import RootLogger


LOGGING_CONFIG = dict(
    version=1,
    disable_existing_loggers=False,
    loggers={
        "VideoStream": {
            "level": "DEBUG",
            "handlers": ["console"]
        }
    },
    handlers={
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "generic",
            "stream": sys.stdout
        }
    },
    formatters={
        "generic": {
            "format": "%(asctime)s - (%(name)s) [%(levelname)s] %(filename)s:%(lineno)d | %(message)s",
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]",
            "class": "logging.Formatter"
        }
    }
)


def set_logging() -> RootLogger:
    logging.config.dictConfig(LOGGING_CONFIG)
    return logging.getLogger()


logger = set_logging()


def print_excp(e: Exception):
    tb = traceback.format_tb(e.__traceback__, 20)
    logger.error(str(e) + '\n' + ''.join(tb))
