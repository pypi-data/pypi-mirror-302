import logging

# Create a module-specific logger
logger = logging.getLogger(__name__)

# Provide a default configuration if no other configuration exists
if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)  # Set default logging level to WARNING

    logger.propagate = False  # Ensure it doesn't propagate to the root logger
