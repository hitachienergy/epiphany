from typing import List

from src.command.command import Command
from src.error import CriticalError


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
            raise CriticalError(f'repquery failed for package `{package}`, reason: package not found')
        elif 'error' in output:
            raise CriticalError(f'repquery failed for package `{package}`, reason: `{output}`')

        packages: List[str] = []
        for line in output.split('\n'):
            if line:
                packages.append(line)

        return packages

