import logging
import os
import shutil
import traceback
from datetime import datetime

class LogManager:
    _instance = None
    _log_initialized = False  # Flag to track initialization

    def __new__(cls, *args, **kwargs):
        """Singleton pattern to ensure only one instance of LogManager"""
        if not cls._instance:
            cls._instance = super(LogManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def _initialize_log(self):
        """Initialize the log configuration"""
        if LogManager._log_initialized:
            return  # Skip if already initialized

        log_dir = 'logs'
        os.makedirs(log_dir, exist_ok=True)

        # If log_current.log exists, move it to log_current_old.log
        if os.path.exists("logs/log_current.log"):
            if os.path.exists("logs/log_current_old.log"):
                os.remove("logs/log_current_old.log")  # Remove the old backup log if it exists
            try:
                shutil.move("logs/log_current.log", "logs/log_current_old.log")
            except PermissionError as e:
                print(f"Error moving log file: {e}")
                # Optionally, log the exception instead of printing
                # logging.exception("Error moving log file")

        # Set up logging to the current log file
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[logging.FileHandler("logs/log_current.log"), logging.StreamHandler()]
        )

        LogManager._log_initialized = True  # Mark as initialized

    def log(self, message, level="INFO"):
        """Log the given message at the specified level"""
        if not LogManager._log_initialized:
            self._initialize_log() # Initialize the log only when needed

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
        if not LogManager._log_initialized:
            self._initialize_log() # Initialize the log only when needed
        error_message = f"Exception: {str(exception)}"
        stack_trace = traceback.format_exc()
        logging.critical(f"{error_message}\nStack Trace:\n{stack_trace}")