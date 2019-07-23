import time
from cli.helpers.Log import Log
from abc import ABCMeta, abstractmethod


class Step(metaclass=ABCMeta):
    def __init__(self, step_name):
        self.logger = Log(step_name)

    def __enter__(self):
        self.start = time.time()
        self.logger.info('Starting run')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        passed = int(round((time.time() - self.start) * 1000))
        self.logger.info('Run done in ' + str(passed) + 'ms')

    @abstractmethod
    def run(self):
        pass
