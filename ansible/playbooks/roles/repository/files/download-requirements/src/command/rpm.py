from typing import List

from src.command.command import Command


class Rpm(Command):
    """
    Interface for `rpm`
    """

    def __init__(self, retries: int):
        super().__init__('rpm', retries)

    def is_package_installed(self, package: str) -> bool:
        """
        Check if `package` is installed on the OS.

        :param package: to be checked if installed
        :returns: True - package installed, False - otherwise
        """
        args: List[str] = ['--query',
                           '--quiet',
                           f'{package}']

        if self.run(args, accept_nonzero_returncode=True).returncode == 0:
            return True

        return False

    def import_key(self, key: str):
        """
        Import pgp key by the `rpm`

        :key: key to be added
        """
        self.run(['--import', key])

    def get_package_capabilities(self, filename: str) -> List[str]:
        args: List[str] = ['-q',
                           '--provides',
                           filename]
        return self._run_and_filter(args)

    def which_packages_provides_file(self, filename: str) -> List[str]:
        args: List[str] = ['-q',
                           '--whatprovides',
                           filename]
        return self._run_and_filter(args)
