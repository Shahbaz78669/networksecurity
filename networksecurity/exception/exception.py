import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):

    def __init__(self, error_message: str, error_detail: sys):
        super().__init__(error_message)

        _, _, exc_tb = sys.exc_info()

        if exc_tb is not None:
            file_name = exc_tb.tb_frame.f_code.co_filename
            line_number = exc_tb.tb_lineno

            self.error_message = (
                f"Error occurred in file [{file_name}] "
                f"at line [{line_number}]: {error_message}"
            )
        else:
            self.error_message = str(error_message)

    def __str__(self):
        return self.error_message

