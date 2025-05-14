from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

def divide_number(a,b):
    try:
        result = a / b
        logger.info("diving two numbers")
        return result

    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise CustomException("An unexpected error occurred",sys)
    
if __name__ == "__main__":
    try:
        logger.info("Starting the division operation")
        divide_number(10, 0)
    except CustomException as e:
        logger.error(str(e))