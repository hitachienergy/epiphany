import logging
import subprocess
from typing import List

from src.error import CriticalError


class Command:
    """
    Interface for running subprocesses
    """

    def __init__(self, process_name: str, retries: int):
        self.__proc_name: str = process_name
        self.__retries: int = retries

    def run(self, args: List[str], capture_output: bool = True) -> subprocess.CompletedProcess:
        """
        Run subprocess with provided arguments

        :param args: additional args which will be used with __proc_name
        :capture_output: save stdout/stderr to completed process object
        :raises: :class:`CriticalError`: when number of retries exceeded
        :returns: completed process object
        """
        process_args = [self.__proc_name]
        process_args.extend(args)

        additional_args = {'encoding': 'utf-8'}
        if capture_output:
            additional_args['stdout'] = subprocess.PIPE
            additional_args['stderr'] = subprocess.PIPE

        for count in range(self.__retries):
            logging.debug(f'[{count + 1}/{self.__retries}] Running: {self.__proc_name} {" ".join(args)} ')

            process = subprocess.run(process_args, **additional_args)

            if process.returncode == 0:
                return process

            logging.warn(process.stderr)

        raise CriticalError('Retries count reached maximum!')
