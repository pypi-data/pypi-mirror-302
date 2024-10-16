import logging

def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Create a console handler
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # Create a simple formatter
    formatter = logging.Formatter('%(levelname)s - %(message)s')

    # Add formatter to ch
    ch.setFormatter(formatter)

    # Add ch to logger
    logger.addHandler(ch)

    return logger
