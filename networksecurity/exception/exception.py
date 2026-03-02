import sys
import os
from networksecurity.logging.logger import logger


class NetworkSecurityException(Exception):

    def __init__(self, error_message: Exception, error_details: sys):
        super().__init__(error_message)

        _, _, exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.file_name = exc_tb.tb_frame.f_code.co_filename
        self.error_message = str(error_message)

    def __str__(self):
        return (
            f"Error occurred in python script "
            f"[{os.path.basename(self.file_name)}] "
            f"line number [{self.lineno}] "
            f"error message [{self.error_message}]"
        )


if __name__ == "__main__":
    try:
        a = 1 / 0
        print("This will not print", a)

    except Exception as e:
        custom_exception = NetworkSecurityException(e, sys)
        logger.error(str(custom_exception))  # force string formatting
        raise custom_exception