from typing import Callable, List

from src.command.command import Command
from src.error import CriticalError, PackageNotfound


class Repoquery(Command):
    """
    Interface for `repoquery`
    """

    def __init__(self, retries: int):
        super().__init__('repoquery', retries)

    def __query(self, package: str,
                queryformat: str,
                arch: str,
                requires: bool,
                resolve: bool,
                quiet: bool,
                output_handler: Callable) -> List[str]:
        """
        Run generic query using `repoquery` tool.

        :param package: data will be returned for this `package`
        :param queryformat: specify custom query output format
        :param arch: limit query output to this architecture
        :param requires: list groups required by group
        :param resolve: resolve dependencies for `package`
        :param output_handler: different queries produce different outputs, use specific output handler
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

        if quiet:
            args.append('--quiet')

        args.extend(['--queryformat', queryformat])
        args.append(f'--archlist={arch},noarch')
        args.append(package)

        output = self.run(args).stdout
        # yumdownloader doesn't set error code if repoquery returns empty output
        output_handler(output)

        packages: List[str] = []
        for line in output.split('\n'):
            if line:
                packages.append(line)

        return packages

    def query(self, package: str, queryformat: str, arch: str) -> List[str]:
        """
        Generic query to yum database.

        :param package: data will be returned for this `package`
        :param queryformat: specify custom query output format
        :param arch: limit query output to this architecture
        :raises:
            :class:`CriticalError`: can be raised on exceeding retries or when error occurred
            :class:`PackageNotfound`: when query did not return any package info
        :returns: query result
        """

        def output_handler(output: str):
            """ In addition to errors, handle missing packages """
            if not output:
                raise PackageNotfound(f'repoquery failed for package `{package}`, reason: package not found, command: `{self.command()}`')
            elif 'error' in output:
                raise CriticalError(f'repoquery failed for package `{package}`, reason: `{output}`, command: `{self.command()}`')

        return self.__query(package, queryformat, arch, False, False, True, output_handler)

    def get_dependencies(self, package: str, queryformat: str, arch: str) -> List[str]:
        """
        Get all dependencies for `package`.

        :param package: data will be returned for this `package`
        :param queryformat: specify custom query output format
        :param arch: limit query output to this architecture
        :raises:
            :class:`CriticalError`: can be raised on exceeding retries or when error occurred
        :returns: query result
        """

        def output_handler(output: str):
            """ Handle errors """
            if 'error' in output:
                raise CriticalError(f'repoquery failed for package `{package}`, reason: `{output}`, command: `{self.command()}`')

        return self.__query(package, queryformat, arch, True, True, True, output_handler)
