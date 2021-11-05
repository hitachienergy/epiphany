from typing import List

from src.command.command import Command


class Yum(Command):
    """
    Interface for `yum`
    """

    def __init__(self, retries: int):
        super().__init__('yum', retries)

    def update(self, enablerepo: str,
                     package: str = None,
                     disablerepo: str = '*',
                     assume_yes: bool = True):
        """
        Interface for `yum update`

        :param enablerepo:
        :param package:
        :param disablerepo:
        :param assume_yes: if set to True, -y flag will be used
        """
        update_parameters: List[str] = ['update']

        update_parameters.append('-y' if assume_yes else '')

        if package is not None:
            update_parameters.append(package)

        update_parameters.append(f'--disablerepo={disablerepo}')
        update_parameters.append(f'--enablerepo={enablerepo}')

        self.run(update_parameters)

    def install(self, package: str,
                assume_yes: bool = True):
        """
        Interface for `yum install -y`

        :param package: packaged to be installed
        :param assume_yes: if set to True, -y flag will be used
        """
        no_ask: str = '-y' if assume_yes else ''
        self.run(['install', no_ask, package])
