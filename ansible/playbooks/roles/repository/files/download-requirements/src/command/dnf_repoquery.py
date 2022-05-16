import re
from typing import Callable, List

from src.command.command import Command
from src.error import CriticalError, PackageNotfound


class DnfRepoquery(Command):
    """
    Interface for `dnf repoquery`
    """

    def __init__(self, retries: int):
        super().__init__('dnf', retries)  # repoquery would require yum-utils package

    def __query(self, defined_packages: List[str],
                queryformat: str,
                archlist: List[str],
                requires: bool,
                resolve: bool,
                output_handler: Callable,
                only_newest: bool = True,
                dependencies: bool = False) -> List[str]:
        """
        Run generic query using `dnf repoquery` command.

        :param defined_packages: data will be returned for those `defined_packages`
        :param queryformat: specify custom query output format
        :param archlist: limit results to these architectures
        :param requires: get capabilities that the defined_packages depend on
        :param resolve: resolve capabilities to originating package(s)
        :param output_handler: different queries produce different outputs, use specific output handler
        :param only_newest: if there are more than one candidate packages, download only the newest one
        :param dependencies: if it's only to grab dependencies
        :raises:
            :class:`CriticalError`: can be raised on exceeding retries or when error occurred
            :class:`PackageNotfound`: when query did not return any package info
        :returns: query result
        """
        args: List[str] = []

        args.append('repoquery')
        args.append(f'--archlist={",".join(archlist)}')
        # to speed up querying
        args.append('--disableplugin=subscription-manager')
        if only_newest:
            args.append('--latest-limit=1')
        args.append(f'--queryformat={queryformat}')

        if requires:
            args.append('--requires')

        if resolve:
            args.append('--resolve')

        args.extend(defined_packages)

        # dnf repoquery doesn't set error code on empty results
        process = self.run(args)

        output_handler(process.stdout, process.stderr)

        packages: List[str] = []
        for line in process.stdout.split('\n'):
            if line:
                packages.append(line)

        if not dependencies:
            missing_packages: List[str] = []
            for package in defined_packages:
                r = re.compile(f'.*{package}')
                match = list(filter(r.match, packages))
                if not match:
                    missing_packages.append(package)
            if missing_packages:
                raise PackageNotfound(
                    f'repoquery failed. Cannot find packages: {missing_packages}')
        return packages

    def query(self, packages: List[str], queryformat: str, archlist: List[str], only_newest: bool = True) -> List[str]:
        """
        Generic query to dnf database.

        :param packages: data will be returned for those `packages`
        :param queryformat: specify custom query output format
        :param archlist: limit results to these architectures
        :param only_newest: if there are more than one candidate packages, download only the newest one
        :raises:
            :class:`CriticalError`: can be raised on exceeding retries or when error occurred
            :class:`PackageNotfound`: when query did not return any package info
        :returns: query result
        """

        def output_handler(output_stdout: str, output_stderr: str):
            """ In addition to errors, handle missing packages """
            if not output_stdout:
                raise PackageNotfound(
                    f'repoquery failed for packages `{packages}`, reason: some of package(s) not found')
            if 'error' in output_stdout:
                raise CriticalError(
                    f'Found an error. repoquery failed for packages `{packages}`, reason: `{output_stdout}`')
            if "Last metadata expiration check" in output_stderr:
                pass  # https://dnf.readthedocs.io/en/latest/conf_ref.html#metadata-expire-label
            elif "No matches found for the following disable plugin patterns: subscription-manager" in output_stderr:
                pass # no subscription-manager on AlmaLinux
            else:
                raise CriticalError(
                    f'repoquery failed for packages `{packages}`, reason: `{output_stderr}`')

        return self.__query(packages, queryformat, archlist, False, False, output_handler, only_newest, False)

    def get_dependencies(self, packages: List[str], queryformat: str, archlist: List[str], only_newest: bool = True) -> List[str]:
        """
        Get all dependencies for `packages`.

        :param packages: data will be returned for those `packages`
        :param queryformat: specify custom query output format
        :param archlist: limit results to these architectures
        :param only_newest: if there are more than one candidate packages, download only the newest one
        :raises:
            :class:`CriticalError`: can be raised on exceeding retries or when error occurred
            :class:`ValueError`: when `packages` list is empty
        :returns: list of dependencies for `packages`
        """
        # repoquery without KEY argument will query dependencies for all packages
        if not packages:
            raise ValueError('packages: list cannot be empty')

        def output_handler(output_stdout: str, output_stderr: str):
            """ In addition to errors, handle missing packages """
            if not output_stdout:
                raise PackageNotfound(
                    f'repoquery failed for packages `{packages}`, reason: some of package(s) not found')
            if 'error' in output_stdout:
                raise CriticalError(
                    f'Found an error. repoquery failed for packages `{packages}`, reason: `{output_stdout}`')
            if "Last metadata expiration check" in output_stderr:
                pass  # https://dnf.readthedocs.io/en/latest/conf_ref.html#metadata-expire-label
            elif output_stderr:
                raise CriticalError(
                    f'repoquery failed for packages `{packages}`, reason: `{output_stderr}`')

        return self.__query(packages, queryformat, archlist, True, True, output_handler, only_newest, True)
