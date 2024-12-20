class ErrorHandler:
    @staticmethod
    def raise_error(file_path, line_number, line_content, error_message):
        """
        Raises a ValueError with the error message, line content, and line number.
        :param file_path: The path of the file where the error occurred.
        :param line_number: The line number where the error occurred.
        :param line_content: The content of the line that caused the error.
        :param error_message: The message describing the error.
        """
        raise ValueError(f"Error in file '{file_path}' at line {line_number + 1}: {error_message}. Line content: `{line_content}`")