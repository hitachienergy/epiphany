from typing import Callable, List

from src.command.command import Command
from src.error import CriticalError, PackageNotfound


class DnfRepoquery(Command):
    """
    Interface for `dnf repoquery`
    """

    def __init__(self, retries: int):
        super().__init__('dnf', retries)  # repoquery would require yum-utils package

    def __query(self, package: str,
                queryformat: str,
                archlist: List[str],
                requires: bool,
                resolve: bool,
                output_handler: Callable) -> List[str]:
        """
        Run generic query using `dnf repoquery` command.

        :param package: data will be returned for this `package`
        :param queryformat: specify custom query output format
        :param archlist: limit results to these architectures
        :param requires: get capabilities that the package depends on
        :param resolve: resolve capabilities to originating package(s)
        :param output_handler: different queries produce different outputs, use specific output handler
        :raises:
            :class:`CriticalError`: can be raised on exceeding retries or when error occurred
            :class:`PackageNotfound`: when query did not return any package info
        :returns: query result
        """
        args: List[str] = []

        args.append('repoquery')
        args.append(f'--archlist={",".join(archlist)}')
        args.append('--assumeyes')  # to import GPG keys
        args.append('--latest-limit=1')
        args.append(f'--queryformat={queryformat}')
        args.append('--quiet')

        if requires:
            args.append('--requires')

        if resolve:
            args.append('--resolve')

        args.append(package)

        output = self.run(args).stdout
        # yumdownloader doesn't set error code if repoquery returns empty output
        output_handler(output)

        packages: List[str] = []
        for line in output.split('\n'):
            if line:
                packages.append(line)

        return packages

    def query(self, package: str, queryformat: str, archlist: List[str]) -> List[str]:
        """
        Generic query to dnf database.

        :param package: data will be returned for this `package`
        :param queryformat: specify custom query output format
        :param archlist: limit results to these architectures
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

        return self.__query(package, queryformat, archlist, False, False, output_handler)

    def get_dependencies(self, package: str, queryformat: str, archlist: List[str]) -> List[str]:
        """
        Get all dependencies for `package`.

        :param package: data will be returned for this `package`
        :param queryformat: specify custom query output format
        :param archlist: limit results to these architectures
        :raises:
            :class:`CriticalError`: can be raised on exceeding retries or when error occurred
        :returns: query result
        """

        def output_handler(output: str):
            """ Handle errors """
            if 'error' in output:
                raise CriticalError(f'repoquery failed for package `{package}`, reason: `{output}`, command: `{self.command()}`')

        return self.__query(package, queryformat, archlist, True, True, output_handler)
