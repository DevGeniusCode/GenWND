from PyQt6.QtWidgets import QMessageBox
from log_manager import LogManager

class ErrorHandler:
    @staticmethod
    def raise_error(file_path, line_number, line_content, error_message, error_level=1):
        """
        Raise an error with a given message and error level.

        :param file_path: Path to the file where the error occurred.
        :param line_number: Line number where the error occurred.
        :param line_content: Content of the line where the error occurred.
        :param error_message: Description of the error.
        :param error_level: Severity level of the error (1: Critical, 2: Non-critical, 3+: Log only).
        """
        log_manager = LogManager()  # Get the singleton log manager

        error_details = f"Error in file '{file_path}'\n at line {line_number + 1}: {error_message}.\n Line content: `{line_content}`"

        if error_level == 1:
            # Critical error
            log_manager.log(f"Critical Error: {error_details}", level="ERROR")
            raise ValueError(error_details)
        elif error_level == 2:
            # Non-critical error, show GUI dialog for skipping or aborting
            log_manager.log(f"Non-Critical Error: {error_details}", level="WARNING")
            response = QMessageBox.warning(
                None,  # Parent widget, None for a toplevel dialog
                "Non-Critical Error",
                f"{error_details}\n\nDo you want to skip this error?",
                QMessageBox.StandardButton.Ignore | QMessageBox.StandardButton.Abort,  # Use Ignore and Abort buttons
                QMessageBox.StandardButton.Ignore  # Default button is 'Skip' (Ignore)
            )

            if response == QMessageBox.StandardButton.Ignore:
                # Skip
                log_manager.log(f"Skipping error: {error_details}", level="WARNING")
                return
            else:
                # Abort
                raise ValueError(error_details)
        else:
            # Log the error without affecting the flow
            log_manager.log(f"Logged Error: {error_details}", level="INFO")
