import logging

def get_logger(name: str):
    # Get a logger instance with the specified name.
    # If a logger with this name already exists, it returns the existing instance.
    logger = logging.getLogger(name)

    # Check if the logger already has any handlers attached.
    # This prevents adding duplicate handlers if get_logger is called multiple times for the same logger name.
    if not logger.handlers:
        # Create a StreamHandler to output log messages to the console (stderr by default).
        handler = logging.StreamHandler()

        # Define the format of the log messages.
        # It includes timestamp, logger name, log level, and the message itself.
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Set the formatter for the handler.
        handler.setFormatter(formatter)

        # Add the configured handler to the logger.
        logger.addHandler(handler)

    # Set the logging level for the logger to INFO.
    # This means only messages with severity INFO, WARNING, ERROR, and CRITICAL will be processed.
    logger.setLevel(logging.INFO)

    # Return the configured logger instance.
    return logger