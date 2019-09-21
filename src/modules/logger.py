import logging
import os


def get_logger():
    project_root = os.path.dirname(os.path.dirname(__file__))
    log_path = os.path.join(project_root, 'logs/main_log.log')
    logger = logging.getLogger('logger')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
