import logging
import logging.handlers
import threading
import os

from pythonjsonlogger import jsonlogger
from cli.helpers.build_io import get_output_path
from cli.helpers.Config import Config

class ColorFormatter(logging.Formatter):
    grey = '\x1b[38;21m'
    yellow = '\x1b[33;21m'
    red = '\x1b[31;21m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    FORMATS = {
        logging.DEBUG: grey + 'format' + reset,
        logging.INFO: grey + 'format' + reset,
        logging.WARNING: yellow + 'format' + reset,
        logging.ERROR: red + 'format' + reset,
        logging.CRITICAL: bold_red + 'format' + reset
    }

    def format(self, record):
        config = Config()
        log_fmt = self.FORMATS.get(record.levelno)
        log_fmt = log_fmt.replace('format', config.log_format)
        formatter = logging.Formatter(log_fmt, datefmt=config.log_date_format)
        return formatter.format(record)


class Log:
    class __LogBase:
        stream_handler = None
        file_handler = None

        def __init__(self):
            config = Config()

            # create stream handler with color formatter
            self.stream_handler = logging.StreamHandler()
            color_formatter = ColorFormatter()
            self.stream_handler.setFormatter(color_formatter)

            # create file handler
            log_path = os.path.join(get_output_path(), config.log_file)
            should_roll_over = os.path.isfile(log_path)
            self.file_handler = logging.handlers.RotatingFileHandler(log_path, backupCount=config.log_count)
            self.file_handler.setLevel(level=logging.INFO)
            if should_roll_over:
                self.file_handler.doRollover()

            # attach propper formatter to file_handler (plain|json)
            if config.log_type == 'plain':
                file_formatter = logging.Formatter(config.log_format, datefmt=config.log_date_format)
                self.file_handler.setFormatter(file_formatter)
            elif config.log_type == 'json':
                json_formatter = jsonlogger.JsonFormatter(config.log_format, datefmt=config.log_date_format)
                self.file_handler.setFormatter(json_formatter)


    instance = None

    def __new__(cls, logger_name):
        if Log.instance is None:
            Log.instance = Log.__LogBase()
        logger = logging.getLogger(logger_name)
        logger.setLevel(level=logging.INFO)
        logger.addHandler(Log.instance.stream_handler)
        logger.addHandler(Log.instance.file_handler)
        return logger


class LogPipe(threading.Thread):

    def __init__(self, logger_name):
        threading.Thread.__init__(self)
        self.logger = Log(logger_name)
        self.daemon = False
        self.fdRead, self.fdWrite = os.pipe()
        self.pipeReader = os.fdopen(self.fdRead)
        self.start()
        self.errorStrings = ['error', 'Error', 'ERROR', 'fatal', 'FAILED']
        self.warningStrings = ['warning', 'warning', 'WARNING']
        self.stderrstrings = []

    def fileno(self):
        return self.fdWrite

    def run(self):
        for line in iter(self.pipeReader.readline, ''):
            line = line.strip('\n')
            if any([substring in line for substring in self.errorStrings]):
                self.stderrstrings.append(line)
                self.logger.error(line)
            elif any([substring in line for substring in self.warningStrings]):
                    self.logger.warning(line)
            else:
                self.logger.info(line)
        self.pipeReader.close()

    def close(self):
        os.close(self.fdWrite)
