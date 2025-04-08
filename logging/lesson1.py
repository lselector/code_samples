
# Python logging 
# https://docs.python.org/3/library/logging.html

import logging
import sys
import time

LOG_FILE = 'myapp.log'
LOG_FORMAT = '%(asctime)sZ - %(name)s - %(levelname)s - %(message)s'

# --- using root logger
logger = logging.getLogger() 
logger.setLevel(logging.DEBUG) 

# --- IMPORTANT: Remove existing handlers if any ---
if logger.hasHandlers():
    print("Clearing existing handlers from root logger...")
    logger.handlers.clear()

# --- Create and configure YOUR handlers ---
# -------------------------------- Formatter -------------------
formatter = logging.Formatter(LOG_FORMAT)
formatter.converter = time.gmtime

# -------------------------------- Console ---------------------
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# -------------------------------- File ------------------------
file_handler = logging.FileHandler(LOG_FILE, mode='a')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# -------------------------------- Logging Examples ------------
logger.debug("debug message")
logger.info("info message")
logger.warning("warning message")
logger.error("error message")
logger.critical("critical message")

# -------------------------------- Exception -------------------
try:
    1/0
except ZeroDivisionError as e:
    logger.exception(f"My_Error_Message : {e}")

# -------------------------------- ShutDown --------------------
logging.shutdown()