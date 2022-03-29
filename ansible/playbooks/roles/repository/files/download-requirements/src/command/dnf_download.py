from pathlib import Path
from typing import List

from src.command.command import Command


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
        args.append('--disableplugin=subscription-manager')  # to speed up download

        if exclude:
            args.append(f'--exclude={exclude}')

        if quiet:
            args.append('--quiet')

        args.append('-y')

        if packages:
            args.extend(packages)
        else:
            raise ValueError('packages: list cannot be empty')

        self.run(args)
