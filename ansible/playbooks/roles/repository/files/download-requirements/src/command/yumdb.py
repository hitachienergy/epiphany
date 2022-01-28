from typing import Dict, List

from src.command.command import Command


class Yumdb(Command):
    """
    Interface for `yumdb`
    """

    def __init__(self, retries: int):
        super().__init__('yumdb', retries)

    def __get_package_info(self, package: str) -> Dict[str, str]:
        """
        Query `package` info and return formatted data.

        :param package: to be checked
        :returns: parsed key/value package data
        """
        args: List[str] = ['info', package]
        info_output = self.run(args).stdout.split('\n')

        info: Dict[str, str] = {}
        for line in info_output[2:]:  # skip first two lines
            if line:
                try:
                    key, val = line.split(' = ')
                    info[key] = val
                except ValueError:
                    pass

        return info

    def get_sha256(self, package: str) -> str:
        return self.__get_package_info(package)['checksum_data']
