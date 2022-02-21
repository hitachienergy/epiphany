from typing import List

from src.command.command import Command


class Pip(Command):
    """
    Interface for `pip` tool.
    """

    def __init__(self, retries: int):
        super().__init__('pip3', retries)

    def install(self, package: str,
                version: str = '',
                user: bool = False) -> bool:
        """
        Interface for `pip install`

        :param package: to install
        :param version: in which version `package` to install
        :param user: install in user's directory
        :returns: True - package had to be installed, False - package already installed
        """
        args: List[str] = ['install']

        if version:
            package = f'{package}{version}'

        args.append(package)

        if user:
            args.append('--user')

        output = self.run(args).stdout

        if f'Requirement already satisfied: {package}' in output:
            return False

        return True

    def uninstall(self, package: str,
                  version: str = '',
                  ensure_yes: bool = True):
        """
        Interface for `pip uninstall`

        :param package: to uninstall
        :param version: in which version `package` to uninstall
        """
        args: List[str] = ['uninstall']

        if version:
            package = f'{package}{version}'

        if ensure_yes:
            args.append('-y')

        args.append(package)

        self.run(args)
