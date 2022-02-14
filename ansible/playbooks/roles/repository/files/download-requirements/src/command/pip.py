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
                user: bool = False):
        """
        Interface for `pip install`

        :param package: to install
        :param version: in which version `package` to install
        :param user: install in user's directory
        """
        args: List[str] = ['install']

        if version:
            package = f'{package}{version}'

        args.append(package)

        if user:
            args.append('--user')

        self.run(args)
