from typing import Callable, List

from src.command.command import Command
from src.error import CriticalError, PackageNotfound


class DnfRepoquery(Command):
    """
    Interface for `dnf repoquery`
    """

    def __init__(self, retries: int):
        super().__init__('dnf', retries)  # repoquery would require yum-utils package

    def __query(self, packages: List[str],
                queryformat: str,
                archlist: List[str],
                requires: bool,
                resolve: bool,
                output_handler: Callable) -> List[str]:
        """
        Run generic query using `dnf repoquery` command.

        :param packages: data will be returned for those `packages`
        :param queryformat: specify custom query output format
        :param archlist: limit results to these architectures
        :param requires: get capabilities that the packages depend on
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
        args.append('--disableplugin=subscription-manager')  # to speed up querying
        args.append('--latest-limit=1')
        args.append(f'--queryformat={queryformat}')
        args.append('--quiet')

        if requires:
            args.append('--requires')

        if resolve:
            args.append('--resolve')

        args.extend(packages)

        output = self.run(args).stdout
        # dnf download doesn't set error code if repoquery returns empty output TODO: verify this
        output_handler(output)

        packages: List[str] = []
        for line in output.split('\n'):
            if line:
                packages.append(line)

        return packages

    def query(self, packages: List[str], queryformat: str, archlist: List[str]) -> List[str]:
        """
        Generic query to dnf database.

        :param packages: data will be returned for those `packages`
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
                raise PackageNotfound(f'repoquery failed for packages `{packages}`, reason: some of package(s) not found')
            elif 'error' in output:
                raise CriticalError(f'repoquery failed for packages `{packages}`, reason: `{output}`')

        return self.__query(packages, queryformat, archlist, False, False, output_handler)

    def get_dependencies(self, packages: List[str], queryformat: str, archlist: List[str]) -> List[str]:
        """
        Get all dependencies for `packages`.

        :param packages: data will be returned for those `packages`
        :param queryformat: specify custom query output format
        :param archlist: limit results to these architectures
        :raises:
            :class:`CriticalError`: can be raised on exceeding retries or when error occurred
        :returns: query result
        """

        def output_handler(output: str):
            """ Handle errors """
            if 'error' in output:
                raise CriticalError(f'repoquery failed for packages `{packages}`, reason: `{output}`')

        return self.__query(packages, queryformat, archlist, True, True, output_handler)
