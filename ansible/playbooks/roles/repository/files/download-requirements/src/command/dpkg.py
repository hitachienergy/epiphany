from typing import List

from src.command.command import Command


class Dpkg(Command):
    """
    Interface for `dpkg`
    """

    def __init__(self, retries: int):
        super().__init__('dpkg', retries)


    def list_installed_packages(self) -> List[str]:
        """
        List all installed packages on the current OS.

        :returns: packages installed on the machine
        """

        proc = self.run(['-l'])
        return proc.stdout.split('\n')
