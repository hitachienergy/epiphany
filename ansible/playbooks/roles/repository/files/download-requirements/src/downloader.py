import logging
from os import chmod
from pathlib import Path
from shutil import move
from tempfile import mkstemp
from typing import Callable, Dict

from src.command.toolchain import Toolchain, TOOLCHAINS
from src.config import Config, OSArch
from src.crypt import SHA_ALGORITHMS
from src.error import CriticalError, ChecksumMismatch


class Downloader:
    """
    Wrapper for downloading requirements with checksum validation.
    """

    def __init__(self, requirements: Dict[str, Dict],
                 sha_algorithm: str,
                 download_func: Callable,
                 download_func_args: Dict = None):
        """
        :param requirements: data from parsed requirements file
        :param sha_algorithm: which algorithm will be used in validating the requirements
        :param download_func: back end function used for downloading the requirements
        :param download_func_args: optional args passed to the `download_func`
        """
        self.__requirements: Dict[str, Dict] = requirements
        self.__sha_algorithm: str = sha_algorithm
        self.__download: Callable = download_func
        self.__download_args: Dict = download_func_args or {}

    def __is_checksum_valid(self, requirement: str, requirement_file: Path) -> bool:
        """
        Check if checksum matches with `requirement` and downloaded file `requirement_file`.

        :param requirement: an entry from the requirements corresponding to the downloaded file
        :param requirement_file: existing requirement file
        :returns: True - checksum ok, False - otherwise
        :raises:
            :class:`ChecksumMismatch`: can be raised on failed checksum and missing allow_mismatch flag
        """
        req = self.__requirements[requirement]
        if req[self.__sha_algorithm] != SHA_ALGORITHMS[self.__sha_algorithm](requirement_file):
            try:
                if req['allow_mismatch']:
                    logging.warning(f'{requirement} - allow_mismatch flag used')
                    return True

                return False
            except KeyError:
                return False

        return True

    def download(self, requirement: str, requirement_file: Path, sub_key: str = None):
        """
        Download `requirement` as `requirement_file` and compare checksums.

        :param requirement: an entry from the requirements corresponding to the downloaded file
        :param requirement_file: existing requirement file
        :param sub_key: optional key for the `requirement` such as `url`
        :raises:
            :class:`ChecksumMismatch`: can be raised on failed checksum
        """
        req = self.__requirements[requirement][sub_key] if sub_key else requirement

        if requirement_file.exists():

            if self.__is_checksum_valid(requirement, requirement_file):
                logging.debug(f'- {requirement} - checksum ok, skipped')
                return
            else:
                logging.info(f'- {requirement}')

                tmpfile = Path(mkstemp()[1])
                chmod(tmpfile, 0o0644)

                self.__download(req, tmpfile, **self.__download_args)

                if not self.__is_checksum_valid(requirement, tmpfile):
                    tmpfile.unlink()
                    raise ChecksumMismatch(f'- {requirement}')

                move(str(tmpfile), str(requirement_file))
                return

        logging.info(f'- {requirement}')
        self.__download(req, requirement_file, **self.__download_args)

        if not self.__is_checksum_valid(requirement, requirement_file):
            requirement_file.unlink()
            raise ChecksumMismatch(f'- {requirement}')
