# --- Imports ---
import logging
import json
import datetime as dt # Import datetime as dt
import traceback
import sys
import time

# -------------------------------- Formatter -------------------
class JSONFormatter(logging.Formatter):
    """
    Formats log records into single-line JSON strings.
    Prepends 'MYWARNING: ' to WARNING messages and 'MYERROR: ' to
    ERROR and CRITICAL messages for easy searching (e.g., with grep).
    """
    def format(self, record: logging.LogRecord) -> str:
        # Create timestamp string, broken down for readability
        timestamp_str = (
            dt.datetime.fromtimestamp(
                record.created, tz=dt.timezone.utc # Use dt here
            )
            .isoformat(timespec='milliseconds')
            .replace('+00:00', 'Z') # Ensure 'Z' for UTC
        )

        # --- Message Modification Logic ---
        original_message = record.getMessage() # Get the formatted message
        output_message = original_message # Default to original

        # Check level and prepend marker string if necessary
        if record.levelno == logging.WARNING:
            output_message = f"MYWARNING: {original_message}"
        elif record.levelno >= logging.ERROR: # Catches ERROR and CRITICAL
            output_message = f"MYERROR: {original_message}"
        # --- End Message Modification ---

        log_record = {
            "timestamp": timestamp_str,
            "level": record.levelname,
            "levelno": record.levelno,
            "message": output_message, # Use the potentially modified message
            "logger_name": record.name,
            "pathname": record.pathname,
            "lineno": record.lineno,
            "funcName": record.funcName,
        }

        # Add exception info if present
        if record.exc_info:
            log_record["traceback"] = self.formatException(
                record.exc_info
            )
            # Also add exception type and specific message for easier parsing
            exc_type, exc_value, tb = record.exc_info
            if exc_value:
                log_record["exception_type"] = exc_type.__name__
                log_record["exception_message"] = str(exc_value)
            # The message field for exceptions already contains MYERROR
            # because logger.exception logs at the ERROR level.

        # Ensure the output is a single line JSON string
        return json.dumps(log_record, default=str, ensure_ascii=False)

# -------------------------------- Logger Setup ----------------
LOG_FILE = 'app_json_markers.log'

logger = logging.getLogger() # Get root logger instance
logger.setLevel(logging.DEBUG) # Set the lowest level to capture

# Clear existing handlers to avoid duplication
if logger.hasHandlers():
    logger.handlers.clear()

# Instantiate the formatter
json_formatter = JSONFormatter() # Use the modified formatter

# -------------------------------- Console Handler -------------
console_handler = logging.StreamHandler(sys.stderr)
console_handler.setLevel(logging.INFO) # Log INFO and above to console
console_handler.setFormatter(json_formatter)
logger.addHandler(console_handler)

# -------------------------------- File Handler ----------------
file_handler = logging.FileHandler(LOG_FILE, mode='a')
file_handler.setLevel(logging.DEBUG) # Log DEBUG and above to file
file_handler.setFormatter(json_formatter)
logger.addHandler(file_handler)

# -------------------------------- Logging Examples ------------
print("--- Running Standard Log Examples ---")
logger.debug("This is a debug message.") # No marker
logger.info("This is an info message.") # No marker
logger.warning("This is a warning message.") # Will have MYWARNING
logger.error("This is an error message.") # Will have MYERROR
logger.critical("This is a critical message.") # Will also have MYERROR
print("--- Standard Log Examples Complete ---")


# -------------------------------- Exception Example -----------
print("\n--- Running Exception Example ---")
try:
    result = 1 / 0
except ZeroDivisionError as e:
    # logger.exception logs at ERROR level, so it will get "MYERROR:"
    logger.exception(f"Calculation failed with ZeroDivisionError: {e}")
print("--- Exception Example Complete ---")


# -------------------------------- Optional: Shutdown -----------
# logging.shutdown()

print(f"\nScript finished. Check console (INFO+) and '{LOG_FILE}' (DEBUG+) for JSON logs.")
print(f"You can now grep the log file, e.g.:")
print(f"  grep MYWARNING {LOG_FILE}")
print(f"  grep MYERROR {LOG_FILE}")