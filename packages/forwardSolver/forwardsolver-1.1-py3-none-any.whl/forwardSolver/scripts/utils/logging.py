import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from forwardSolver.scripts.utils.constants import LOG_DIR


def get_logger(name: str, level: int = logging.DEBUG):
    """
    Create a logger with name `name` and logging level `level`.
    The logger will automatically have a stream and filehandler attached.
    Returns the logger.
    Args:
        name (str): The name of the logger.
        level (int, optional): The logging level. Defaults to logging.DEBUG.
    Returns:
        logging.Logger: Configured logger instance.
    """

    # Create log directory if it does not exist
    Path(LOG_DIR).mkdir(exist_ok=True)

    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # create console handler and set level to debug
    # stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(level)

    # file handler
    filename = Path(LOG_DIR, name)
    file_handler = RotatingFileHandler(filename.as_posix() + ".log", maxBytes=100000)
    file_handler.setLevel(level)

    # create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # add formatter to stream and file
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # add stream to logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)

    return logger


def close_logger(logger: logging.Logger):
    """
    Closes and removes all handlers from logger with name `name`.
    Args:
        logger (logging.Logger): The logger whose handlers are to be closed and removed.
    """

    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)


def close_all_loggers():
    """
    Close all loggers found in the `LOG_DIR`
    Note:
        - LOG_DIR should be defined as the directory containing the log files.
        - The function `close_logger` should be defined to handle the closing of individual loggers.
    Raises:
        FileNotFoundError: If the LOG_DIR does not exist.
        Exception: If there is an issue closing any of the loggers.
    """

    logs = Path(LOG_DIR)
    for logfile in logs.glob("*"):
        # get name of logger from logfile
        logname = logfile.name.split(".log")[0]
        log = logging.getLogger(logname)
        close_logger(log)
