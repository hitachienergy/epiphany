from typing import List

from src.command.command import Command
from src.error import CriticalError, PackageNotfound


class Repoquery(Command):
    """
    Interface for `repoquery`
    """

    def __init__(self, retries: int):
        super().__init__('repoquery', retries)

    def query(self, package: str,
              queryformat: str,
              arch: str,
              requires: bool = False,
              resolve: bool = False) -> List[str]:
        """
        Run generic query using `repoquery` tool.

        :param package: data will be returned for this `package`
        :param queryformat: specify custom query output format
        :param arch: limit query output to this architecture
        :param requires: list groups required by group
        :param resolve: resolve dependencies for `package`
        :raises:
            :class:`CriticalError`: can be raised on exceeding retries or when error occurred
            :class:`PackageNotfound`: when query did not return any package info
        :returns: query result
        """
        args: List[str] = []

        if requires:
            args.append('--requires')

        if resolve:
            args.append('--resolve')

        args.extend(['--queryformat', queryformat])
        args.append(f'--archlist={arch},noarch')
        args.append(package)

        output = self.run(args).stdout
        # yumdownloader doesn't set error code if repoquery returns empty output
        if not output:
            raise PackageNotfound(f'repquery failed for package `{package}`, reason: package not found')
        elif 'error' in output:
            raise CriticalError(f'repquery failed for package `{package}`, reason: `{output}`')

        packages: List[str] = []
        for line in output.split('\n'):
            if line:
                packages.append(line)

        return packages

