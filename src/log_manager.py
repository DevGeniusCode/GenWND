import logging
import os
import shutil
import traceback
from datetime import datetime

class LogManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Singleton pattern to ensure only one instance of LogManager"""
        if not cls._instance:
            cls._instance = super(LogManager, cls).__new__(cls, *args, **kwargs)
            cls._instance._initialize_log()  # This is called once when the first instance is created
        return cls._instance

    def _initialize_log(self):
        """Initialize the log configuration"""
        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)

        # If log_current.log exists, move it to log_current_old.log
        if os.path.exists("logs/log_current.log"):
            if os.path.exists("logs/log_current_old.log"):
                os.remove("logs/log_current_old.log")  # Remove the old backup log if it exists
            shutil.move("logs/log_current.log", "logs/log_current_old.log")

        # Set up logging to the current log file
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[logging.FileHandler("logs/log_current.log"), logging.StreamHandler()]
        )

    def log(self, message, level="INFO"):
        """Log the given message at the specified level"""
        log_function = {
            "DEBUG": logging.debug,
            "INFO": logging.info,
            "WARNING": logging.warning,
            "ERROR": logging.error,
            "CRITICAL": logging.critical
        }.get(level.upper(), logging.info)

        log_function(message)

    def log_exception(self, exception):
        """Log an exception with stack trace"""
        error_message = f"Exception: {str(exception)}"
        stack_trace = traceback.format_exc()
        logging.critical(f"{error_message}\nStack Trace:\n{stack_trace}")
