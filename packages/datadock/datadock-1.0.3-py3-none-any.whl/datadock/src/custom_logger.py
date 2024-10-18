# Custom logger for logging
from pathlib import Path
import logging


class CustomLogger:

    def __init__(
        self,
        logger=None,
        log_file_name: str = "default.log",
        log_dir_path: str | Path = None,
        logging_name: str = "logging",
    ) -> None:
        # if no log directory is provided, use a default directory to the current path
        if log_dir_path is None:
            log_dir_path = (
                Path(__file__).resolve().parent.parent.parent / "DataDockLogs"
            )
        else:
            log_dir_path = Path(log_dir_path)

        # construct full path to the log file
        log_file_path = log_dir_path / log_file_name
        # checks if the directory exists
        if not log_dir_path.exists():
            log_dir_path.mkdir(parents=True, exist_ok=True)

        self.logger = logging.getLogger(logging_name)
        self.logger.setLevel(logging.DEBUG)

        # Prevent additional multiple logging handlers
        if not self.logger.handlers:
            # Create a file handler and set level to debug
            self.file_handler = logging.FileHandler(log_file_path)
            self.file_handler.setLevel(logging.DEBUG)

            # # Create console handler to output logs to the console
            # console_handler = logging.StreamHandler()
            # console_handler.setLevel(logging.DEBUG)

            # Define a log format
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            self.file_handler.setFormatter(formatter)
            # console_handler.setFormatter(formatter)

            # Add handlers to the logger
            self.logger.addHandler(self.file_handler)
            # self.logger.addHandler(console_handler)

    def _log_with_status(self, level, message, status):
        # Log the message with status included
        extra = {"status": status}  # Provide 'status' as extra info for formatter
        if level == logging.DEBUG:
            self.logger.debug(message, extra=extra)
        elif level == logging.INFO:
            self.logger.info(message, extra=extra)
        elif level == logging.WARNING:
            self.logger.warning(message, extra=extra)
        elif level == logging.ERROR:
            self.logger.error(message, extra=extra)
        elif level == logging.CRITICAL:
            self.logger.critical(message, extra=extra)

    def debug(self, message: str, status: int = 100):
        # Log debug messages
        self._log_with_status(logging.DEBUG, message, status)

    def info(self, message: str, status: int = 200):
        # Log info messages
        self._log_with_status(logging.INFO, message, status)

    def warning(self, message: str, status: int = 400):
        # Log warning messages
        self._log_with_status(logging.WARNING, message, status)

    def error(self, message: str, status: int = 401):
        # Log error messages
        self._log_with_status(logging.ERROR, message, status)

    def critical(self, message: str, status: int = 500):
        # Log critical messages
        self._log_with_status(logging.CRITICAL, message, status)
