import logging
import subprocess
from typing import List

from src.error import RetriesExceeded


class Command:
    """
    Interface for running subprocesses
    """

    def __init__(self, process_name: str, retries: int, pipe_args: List[str] = None):
        self.__proc_name: str = process_name
        self.__retries: int = retries
        self.__pipe_args: List[str] = pipe_args  # used for __or__
        self.__command: str = ''

    def name(self) -> str:
        return self.__proc_name

    def pipe_args(self) -> List[str]:
        return self.__pipe_args or []

    def command(self) -> str:
        return self.__command

    def run(self, args: List[str],
            capture_output: bool = True,
            accept_nonzero_returncode: bool = False) -> subprocess.CompletedProcess:
        """
        Run subprocess with provided arguments

        :param args: additional args which will be used with __proc_name
        :capture_output: save stdout/stderr to completed process object
        :raises: :class:`RetriesExceeded`: when number of retries exceeded
        :returns: completed process object
        """
        process_args = [self.__proc_name]
        process_args.extend(args)

        self.__command = f'{self.__proc_name} {" ".join(args)}'

        additional_args = {'encoding': 'utf-8'}
        if capture_output:
            additional_args['stdout'] = subprocess.PIPE
            additional_args['stderr'] = subprocess.PIPE

        for count in range(self.__retries):
            logging.debug(f'[{count + 1}/{self.__retries}] Running: `{self.__command}`')

            process = subprocess.run(process_args, **additional_args)

            if accept_nonzero_returncode:
                return process

            if process.returncode == 0:
                return process

            if process.stderr:
                logging.warning(process.stderr)

        raise RetriesExceeded(f'Retries count reached maximum, command: `{self.__command}`')

    def __or__(self, command) -> str:
        """
        Run two subprocesses by piping output from the first process to the second process.

        :param command: process onto which output from the first process will be passed
        :raises: :class:`RetriesExceeded`: when number of retries exceeded
        :returns: final stdout
        """
        lproc_name = f'{self.__proc_name} {" ".join(self.__pipe_args)}'
        rproc_name = f'{command.name()} {" ".join(command.pipe_args())}'
        self.__command = f'{lproc_name} | {rproc_name}'

        for count in range(self.__retries):
            logging.debug(f'[{count + 1}/{self.__retries}] Running: `{self.__command}`')

            lproc = subprocess.Popen([self.__proc_name] + self.__pipe_args, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            rproc = subprocess.Popen([command.name()] + command.pipe_args(), stdin=lproc.stdout, stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)
            lproc.stdout.close()  # Allow proc1 to receive a SIGPIPE if proc2 exits.

            output = rproc.communicate()[0].decode()
            if rproc.returncode == 0:
                return output

            logging.warning(lproc.stderr if lproc.returncode != 0 else rproc.stderr)

        raise RetriesExceeded(f'Retries count reached maximum, command: `{self.__command}`')

    def _run_and_filter(self, args: List[str]) -> List[str]:
        """
        Run subprocess and return list of filtered stdout lines

        :param args: run subprocess with these args
        :returns: filtered output lines from the subprocess stdout
        """
        raw_output = self.run(args).stdout
        return list(filter(lambda elem: elem != '', raw_output.split('\n')))  # filter empty lines
