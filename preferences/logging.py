import logging
import coloredlogs
import os
from preferences import paths

def setup():
    # Check if the logging has already been configured
    if not logging.root.handlers:
        coloredlogs.install(level="INFO", logger=logging.getLogger(__name__), fmt="%(levelname)s: %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        file_handler = logging.FileHandler(os.path.join(paths.app(), 'log_errors.log'))
        file_handler.setLevel(logging.ERROR)
        file_formatter = logging.Formatter("---\n%(asctime)s %(levelname)-8s %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
        file_handler.setFormatter(file_formatter)

        logger = logging.getLogger(__name__)
        logger.addHandler(file_handler)

        return logger

    else:
        # Logging is already configured, return the existing logger and handler
        logger = logging.getLogger(__name__)
        console_handler = logger.handlers[0]  # Assuming the console handler is the first one
        return logger

if __name__ == '__main__':
    print("Please run pybutler.py")