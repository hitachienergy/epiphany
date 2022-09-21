import logging
from os import chmod
from pathlib import Path
from shutil import move
from tempfile import mkstemp
from typing import Callable, Dict

from src.crypt import SHA_ALGORITHMS
from src.error import ChecksumMismatch


class BaseDownloader:
    """
    Wrapper for downloading requirements with checksum validation.
    """

    def __init__(self, requirements: Dict[str, Dict],
                 sha_algorithm: str,
                 download_func: Callable,
                 download_func_args: Dict = None,
                 check_connection: Callable = None):
        """
        :param requirements: data from parsed requirements file
        :param sha_algorithm: which algorithm will be used in validating the requirements
        :param download_func: back end function used for downloading the requirements
        :param download_func_args: optional args passed to the `download_func`
        :param check_connection: optional function for checking connection to downloaded requirements
        """
        self._requirements: Dict[str, Dict] = requirements
        self.__sha_algorithm: str = sha_algorithm
        self.__download: Callable = download_func
        self.__download_args: Dict = download_func_args or {}
        self.__check_connection: Callable = check_connection or (lambda addr: True)

    def __is_checksum_valid(self, requirement: str, requirement_file: Path) -> bool:
        """
        Check if checksum matches with `requirement` and downloaded file `requirement_file`.

        :param requirement: an entry from the requirements corresponding to the downloaded file
        :param requirement_file: existing requirement file
        :returns: True - checksum ok, False - otherwise
        """
        if requirement[self.__sha_algorithm] != SHA_ALGORITHMS[self.__sha_algorithm](requirement_file):
            try:
                if requirement['allow_mismatch']:
                    logging.warning(f'{requirement} - allow_mismatch flag used')
                    return True

                return False
            except KeyError:
                return False

        return True

    def _download(self, requirement: str, address: str, requirement_file: Path, additional_args: dict = None) -> bool:
        """
        Download `requirement` as `requirement_file` and compare checksums.

        :param requirement: an entry from the requirements corresponding to the downloaded file
        :param address: an adress at which the requirement is available
        :param requirement_file: existing requirement file
        :param sub_key: optional key for the `requirement` such as `url`
        :param additional_args: optional arguments passed to `download_func`
        :raises:
            :class:`ChecksumMismatch`: can be raised on failed checksum
        :returns: True - file downloaded correctly and/or checksum matched, False - otherwise
        """
        additional_args = additional_args or {}
        download_args = {**self.__download_args, **additional_args}

        if requirement_file.exists():
            if self.__is_checksum_valid(requirement, requirement_file):
                logging.debug(f'- {address} - checksum ok, skipped')
                return True

            logging.info(f'- {address}')

            tmpfile = Path(mkstemp()[1])
            chmod(tmpfile, 0o0644)

            if not self.__check_connection(address):
                return False

            self.__download(address, tmpfile, **download_args)

            if not self.__is_checksum_valid(requirement, tmpfile):
                tmpfile.unlink()
                raise ChecksumMismatch(f'- {address}')

            move(str(tmpfile), str(requirement_file))
            return True

        logging.info(f'- {address}')
        if not self.__check_connection(address):
            return False

        self.__download(address, requirement_file, **download_args)

        if not self.__is_checksum_valid(requirement, requirement_file):
            requirement_file.unlink()
            raise ChecksumMismatch(f'- {address}')

        return True
