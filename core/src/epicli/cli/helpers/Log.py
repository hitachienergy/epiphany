import logging
import threading
import os
from pythonjsonlogger import jsonlogger
from cli.helpers.build_saver import get_output_path

LOG_FILE = 'log.json'
LOG_FORMAT = '%(asctime)s %(levelname)s %(name)s - %(message)s'
LOG_DATE_FMT = '%H:%M:%S'


class Log:
    class __LogBase:
        json_handler = None

        def __init__(self):
            logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt=LOG_DATE_FMT)
            formatter = jsonlogger.JsonFormatter(LOG_FORMAT, datefmt=LOG_DATE_FMT)
            self.json_handler = logging.FileHandler(filename=os.path.join(get_output_path(), LOG_FILE))
            self.json_handler.setFormatter(formatter)

    instance = None

    def __new__(cls, logger_name):
        if Log.instance is None:
            Log.instance = Log.__LogBase()
        logger = logging.getLogger(logger_name)
        logger.addHandler(Log.instance.json_handler)
        return logger


class LogPipe(threading.Thread):

    def __init__(self, logger_name):
        threading.Thread.__init__(self)
        self.logger = Log(logger_name)
        self.daemon = False
        self.fdRead, self.fdWrite = os.pipe()
        self.pipeReader = os.fdopen(self.fdRead)
        self.start()

    def fileno(self):
        return self.fdWrite

    def run(self):
        for line in iter(self.pipeReader.readline, ''):
            self.logger.info(line.strip('\n'))
        self.pipeReader.close()

    def close(self):
        os.close(self.fdWrite)



