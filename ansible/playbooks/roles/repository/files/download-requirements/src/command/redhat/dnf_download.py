from pathlib import Path
from typing import List

from src.command.command import Command
from src.error import CriticalError


class DnfDownload(Command):
    """
    Interface for `dnf download`
    """

    def __init__(self, retries: int):
        super().__init__('dnf', retries)

    def download_packages(self, packages: List[str],
                          archlist: List[str],
                          destdir: Path,
                          exclude: str = '',
                          quiet: bool = True):
        args: List[str] = ['download']

        args.append(f'--archlist={",".join(archlist)}')
        args.append(f'--destdir={str(destdir)}')
        # to speed up download
        args.append('--disableplugin=subscription-manager')

        if exclude:
            args.append(f'--exclude={exclude}')

        if quiet:
            args.append('--quiet')

        args.append('-y')
        args.extend(packages)

        process = self.run(args)
        if 'error' in process.stdout:
            raise CriticalError(
                f'Found an error. dnf download failed for packages `{packages}`, reason: `{process.stdout}`')
        if process.stderr:
            raise CriticalError(
                f'dnf download failed for packages `{packages}`, reason: `{process.stderr}`')
