import time
from abc import ABCMeta

from cli.helpers.Log import Log
from cli.helpers.time_helpers import format_time


class Step(metaclass=ABCMeta):
    def __init__(self, step_name):
        self.logger = Log(step_name)

    def __enter__(self):
        self.start = time.time()
        self.logger.info('Starting step')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        passed_time = format_time(time.time()-self.start)
        self.logger.info(f'Step finished in: {passed_time}')
