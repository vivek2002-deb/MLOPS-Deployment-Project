import traceback  ## for tracking the error
import sys

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        super().__init__(error_message)
        self.message = self.get_detailed_error_message(error_message, error_detail=error_detail)

    @staticmethod
    def get_detailed_error_message(error_message,error_detail: sys) -> str:
        _, _, exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        error_message = f"Error occurred in script: {file_name} at line number: {line_number}"
        return error_message

    def __str__(self):
        return self.message
