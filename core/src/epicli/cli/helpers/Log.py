import logging
import logging.handlers
import threading
import os
from pythonjsonlogger import jsonlogger
from cli.helpers.build_saver import get_output_path
from cli.helpers.Config import Config


class Log:
    class __LogBase:
        json_file_handler = None
        json_stream_handler = None

        def __init__(self):
            config = Config()
            log_path = os.path.join(get_output_path(), config.log_file)
            logging.basicConfig(level=logging.INFO, format=config.log_format, datefmt=config.log_date_format)
            formatter = jsonlogger.JsonFormatter(config.log_format, datefmt=config.log_date_format)
            self.json_file_handler = logging.FileHandler(filename=log_path)
            self.json_file_handler.setFormatter(formatter)
            self.json_stream_handler = logging.StreamHandler()
            self.json_stream_handler.setFormatter(formatter)
            should_roll_over = os.path.isfile(log_path)
            handler = logging.handlers.RotatingFileHandler(log_path, mode='w', backupCount=config.log_count)
            if should_roll_over:
                handler.doRollover()

    instance = None

    def __new__(cls, logger_name):
        if Log.instance is None:
            Log.instance = Log.__LogBase()
        config = Config()
        logger = logging.getLogger(logger_name)
        if config.log_type == 'json':
            logger.addHandler(Log.instance.json_stream_handler)
        logger.addHandler(Log.instance.json_file_handler)
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



