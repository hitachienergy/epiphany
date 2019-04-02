import logging
from abc import ABCMeta, abstractmethod


class Step(metaclass=ABCMeta):
    def __init__(self, step_name):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(step_name)

    def __enter__(self):
        self.logger.info('Starting')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.logger.info('Done\n')

    @abstractmethod
    def run(self):
        pass
