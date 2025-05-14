import logging
import os
from datetime import datetime
from colorlog import ColoredFormatter

# Create logs directory
log_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(log_dir, exist_ok=True)

# Define log file name
log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_file_path = os.path.join(log_dir, log_file)

# File handler
file_handler = logging.FileHandler(log_file_path)
file_handler.setFormatter(logging.Formatter("[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"))

# Console handler 
console_handler = logging.StreamHandler()
color_formatter = ColoredFormatter(
    "%(log_color)s[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    log_colors={
        'DEBUG':    'cyan',
        'INFO':     'green',
        'WARNING':  'yellow',
        'ERROR':    'red',
        'CRITICAL': 'bold_red',
    }
)
console_handler.setFormatter(color_formatter)

# Get logger
logger = logging.getLogger("nids_logger")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.propagate = False
