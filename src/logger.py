import logging
import os
from datetime import datetime

def setup_logging():

    # Generate log file name with timestamp
    LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

    # Create "logs" directory if it doesn't exist
    logs_dir = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Full path to the log file
    LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

    # Set up logging
    logging.basicConfig(
        filename=LOG_FILE_PATH,
        format='[ %(asctime)s ] %(filename)s: %(lineno)d %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )