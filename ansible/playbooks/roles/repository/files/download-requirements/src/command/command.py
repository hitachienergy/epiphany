import logging
import subprocess
from typing import List

from src.error import CriticalError


class Command:
    """
    Interface for running subprocesses
    """

    def __init__(self, process_name: str, retries: int, pipe_args: List[str] = None):
        self.__proc_name: str = process_name
        self.__retries: int = retries
        self.__pipe_args: List[str] = pipe_args  # used for __pipe__

    def name(self) -> str:
        return self.__proc_name

    def pipe_args(self) -> List[str]:
        return self.__pipe_args or []

    def run(self, args: List[str],
            capture_output: bool = True,
            accept_nonzero_returncode: bool = False) -> subprocess.CompletedProcess:
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

            if accept_nonzero_returncode:
                return process

            if process.returncode == 0:
                return process

            logging.warn(process.stderr)

        raise CriticalError('Retries count reached maximum!')

    def __or__(self, command) -> str:
        """
        Run two subprocesses by piping output from the first process to the second process.

        :param command: process onto which output from the first process will be passed
        :raises: :class:`CriticalError`: when number of retries exceeded
        :returns: final stdout
        """
        lproc_name = f'{self.__proc_name} {" ".join(self.__pipe_args)}'
        rproc_name = f'{command.name()} {" ".join(command.pipe_args())}'
        whole_process_name = f'{lproc_name} | {rproc_name}'

        for count in range(self.__retries):
            logging.debug(f'[{count + 1}/{self.__retries}] Running: {whole_process_name}')

            lproc = subprocess.Popen([self.__proc_name] + self.__pipe_args, stdout=subprocess.PIPE)
            rproc = subprocess.Popen([command.name()] + command.pipe_args(), stdin=lproc.stdout, stdout=subprocess.PIPE)
            lproc.stdout.close()  # Allow proc1 to receive a SIGPIPE if proc2 exits.

            output = rproc.communicate()[0].decode()
            if rproc.returncode == 0:
                return output

            logging.warn(lproc.stderr if not lproc.returncode == 0 else rproc.stderr)

        raise CriticalError('Retries count reached maximum!')
