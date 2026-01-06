import sys
import os
import logging
from src.config import BASEDIR, SET_CONF
from src.utils.singleton import SingletonMeta
from logging.handlers import RotatingFileHandler


class AppLogger(metaclass=SingletonMeta):
    def __init__(self, log_filename: str | None = None):
        """
        Initializes the logger.
        Note: Due to SingletonMeta, this might be called multiple times,
        but we protect against duplicate handlers.
        """

        ### GENERAL LOGGING SETTINGS
        self.logger = logging.getLogger(__name__)
        if self.logger.handlers:
            return
        if not log_filename:  # Fallback
            log_filename = os.path.join(BASEDIR, "logs", "logs.log")
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

        ### CONSOLE
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(SET_CONF.LOG_LEVEL)
        stdout_handler.setFormatter(formatter)

        ### LOGDFILE
        # create Log-dir if not existing
        log_dir = os.path.dirname(log_filename)
        os.makedirs(log_dir, exist_ok=True)

        file_handler = RotatingFileHandler(
            log_filename,
            mode="a",
            maxBytes=5 * 1024 * 1024,
            backupCount=5,
            encoding=None,
            delay=0,
        )

        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(stdout_handler)

    # direct redirects to Logger-Methods
    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs, stacklevel=2)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs, stacklevel=2)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs, stacklevel=2)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs, stacklevel=2)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs, stacklevel=2)

    def exception(self, msg, *args, **kwargs):
        """Log a msg with Level ERROR and add Exception-Info"""
        self.logger.exception(msg, *args, **kwargs, stacklevel=2)


logfile_path = os.path.join(BASEDIR, "logs", "logs.log")
logmsg = AppLogger(log_filename=logfile_path)
