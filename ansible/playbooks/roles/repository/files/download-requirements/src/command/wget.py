from enum import Enum
from pathlib import Path
from typing import List

from src.command.command import Command


class IPFamily(Enum):
    IPV4 = 'IPv4'
    IPV6 = 'IPv6'


class Wget(Command):
    """
    Interface for `wget`
    """

    def __init__(self, retries: int):
        super().__init__('wget', retries)
        self.__download_params: List[str] = [
            '--no-use-server-timestamps',
            '--show-progress'
        ]

    def check_connection(self, url: str) -> bool:
        """
        Use wget in a spider mode to check whether the file can be downloaded or not.

        :param url: address which will be checked
        :returns: True - connection valid, False - otherwise
        """
        params: List[str] = ['-q', '--spider']

        if not self.run(params + [url]).returncode:
            return True

        return False

    def download(self, url: str,
                 output_document: Path = None,
                 directory_prefix: Path = None,
                 ip_family: IPFamily = IPFamily.IPV4,
                 additional_params: bool = True):
        """
        Download target file

        :param url: file to be downloaded
        :param output_document: downloaded file will be stored under this path
        :param directory_prefix: downloaded file will be stored under this path, keep original filename
        :param ip_family: which IP version to be used
        """
        output_params: List[str] = []
        if additional_params:
            output_params.extend(self.__download_params)

        if output_document is not None:
            output_params.append(f'--output-document={str(output_document)}')

        if directory_prefix is not None:
            output_params.append(f'--directory-prefix={str(directory_prefix)}')

        output_params.append(f'--prefer-family={ip_family.value}')

        self.run(output_params + [url])
