import logging

LOGGING_FILE = "logging.log"

logging.basicConfig(filename=LOGGING_FILE,
    filemode='a',
    format='[%(asctime)s][%(name)s] %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO)

def get_logger(name):
    return logging.getLogger(name)