import logging      # Import Python's built-in logging module to handle log messages
import sys          # Import sys module to access system-specific parameters and functions
def setup_logging():
# Set up basic configuration for logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
logger = logging.getLogger("Medbuddy") # Create a logger instance named "Medbuddy" which we will use throughout the app to write logs
