import sys
from src.logging.logger import logger

def get_error_message_detail(error, error_detail: sys):
    """
    Generates a  detailed error message including the script name, line number, and error message.

    Args:
        error: The exception/error object.
        error_detail: The sys module to extract exception details.

    Returns:
        str: A formatted error message with script name, line number, and error message.
    """
    try:
        exc_type, exc_obj, exc_tb = error_detail.exc_info()

        if exc_tb is not None:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno
        else:
            file_name = "Unknown"
            line_number = "Unknown"

        error_message = (
            f"Exception in script: [{file_name}] "
            f"at line: [{line_number}] "
            f"with error: [{str(error)}]"
        )
        logger.error(error_message)
        return error_message

    except Exception as internal_error:
        logger.error(f"Error while generating detailed error message: {internal_error}")
        return f"Failed to generate detailed error message: {str(error)}"

class CustomException(Exception):
    """
    Custom exception class for the Network Intrusion Detection ML Project.

    Args:
        error_message: The error message or exception object.
        error_detail: The sys module to extract exception details.
    """
    def __init__(self, error_message, error_detail: sys):
        super().__init__(str(error_message))
        
        # Generate a detailed error message
        self.error_message = get_error_message_detail(error_message, error_detail)

    def __str__(self):
        """
        Return the detailed error message string representation.
        """
        return self.error_message
