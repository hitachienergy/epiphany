import logging
import logging.handlers
import os
import threading

import click
from pythonjsonlogger import jsonlogger

from cli.src.Config import Config
from cli.src.helpers.build_io import get_output_path


class ColorFormatter(logging.Formatter):
    FORMATS = {
        logging.DEBUG:    click.style('format', fg=8), # grey
        logging.INFO:     click.style('format'),
        logging.WARNING:  click.style('format', fg='yellow'),
        logging.ERROR:    click.style('format', fg='red'),
        logging.CRITICAL: click.style('format', fg='red', bold=True)
    }

    def format(self, record):
        config = Config()
        log_fmt = self.FORMATS.get(record.levelno)
        log_fmt = log_fmt.replace('format', config.log_format)
        formatter = logging.Formatter(log_fmt, datefmt=config.log_date_format)
        return formatter.format(record)


class UncolorFormatter(logging.Formatter):
    """
    Formatter that removes ANSI styling information (escape sequences).
    """
    def format(self, record: logging.LogRecord) -> str:
        return click.unstyle(super().format(record))


class UncolorJsonFormatter(jsonlogger.JsonFormatter):
    """
    JSON formatter that removes ANSI styling information (escape sequences).
    """
    def format(self, record: logging.LogRecord) -> str:
        return click.unstyle(super().format(record))


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
                file_formatter = UncolorFormatter(config.log_format, datefmt=config.log_date_format)
                self.file_handler.setFormatter(file_formatter)
            elif config.log_type == 'json':
                json_formatter = UncolorJsonFormatter(config.log_format, datefmt=config.log_date_format)
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
        self.fd_read, self.fd_write = os.pipe()
        self.pipe_reader = os.fdopen(self.fd_read)
        self.start()
        self.error_strings = ['error', 'Error', 'ERROR', 'fatal', 'FAILED']
        self.warning_strings = ['warning', 'warning', 'WARNING']
        self.stderr_strings = []

    def fileno(self):
        return self.fd_write

    def run(self):
        """Run thread logging everything."""
        for line in iter(self.pipe_reader.readline, ''):
            line = line.strip('\n')
            if any([substring in line for substring in self.error_strings]):
                self.stderr_strings.append(line)
                self.logger.error(line)
            elif any([substring in line for substring in self.warning_strings]):
                self.logger.warning(line)
            else:
                self.logger.info(line)
        self.pipe_reader.close()

    def close(self):
        os.close(self.fd_write)
