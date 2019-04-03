import logging
import os
from pythonjsonlogger import jsonlogger

# todo make logfile configurable?
LOG_FILE = os.path.dirname(__file__) + '/../../output/log.json'
LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s - %(message)s'
LOG_DATE_FMT = '%H:%M:%S'

class Log:
    json_handler = None

    @classmethod
    def setup_logging(self, log_level):
        logging.basicConfig(level=log_level, format=LOG_FORMAT, datefmt=LOG_DATE_FMT)
        formatter = jsonlogger.JsonFormatter(LOG_FORMAT, datefmt=LOG_DATE_FMT)
        self.json_handler = logging.FileHandler(filename=LOG_FILE)
        self.json_handler.setFormatter(formatter)

    @classmethod
    def get_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.addHandler(self.json_handler)
        return logger




