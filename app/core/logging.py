import logging      # Import Python's built-in logging module to handle log messages
import sys          # Import sys module to access system-specific parameters and functions
def setup_logging():
# Set up basic configuration for logging
    logging.basicConfig(
        level=logging.INFO,    # Show all messages with level INFO and above (like warnings and errors)
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",  # Define how log messages will look (time, level, source, message)
        handlers=[
            logging.StreamHandler(sys.stdout)  # Send the log output to the console (standard output)
        ]
    )
logger = logging.getLogger("Medbuddy") # Create a logger instance named "Medbuddy" which we will use throughout the app to write logs
