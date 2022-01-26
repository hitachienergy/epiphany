from pathlib import Path
from typing import List

from src.command.command import Command


class Yumdownloader(Command):
    """
    Interface for `yumdownloader`
    """

    def __init__(self, retries: int):
        super().__init__('yumdownloader', retries)

    def download_packages(self, packages: List[str],
                          arch: str,
                          exclude: str,
                          destdir: Path,
                          quiet: bool = True):
        args: List[str] = []

        if quiet:
            args.append('--quiet')

        args.append(f'--archlist={arch}')
        args.append(f'--exclude={exclude}')
        args.append(f'--destdir={str(destdir)}')
        args.extend(packages)

        self.run(args)
