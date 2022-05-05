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
        args.append('--disableplugin=subscription-manager')  # to speed up download

        if exclude:
            args.append(f'--exclude={exclude}')

        if quiet:
            args.append('--quiet')

        args.append('-y')
        args.extend(packages)

        output_stdout = self.run(args).stdout
        output_stderr = self.run(args).stderr

        def output_handler(output_stdout: str, output_stderr: str):
                    """ In addition to errors, handle missing packages
                    :raises:
                        :class:`CriticalError`: raised when error occurred
                    """
                    if 'error' in output_stdout:
                        raise CriticalError(f'Found an error. dnf download failed for packages `{packages}`, reason: `{output_stdout}`')
                    if output_stderr:
                        raise CriticalError(f'dnf download failed for packages `{packages}`, reason: `{output_stderr}`')


        output_handler(output_stdout, output_stderr)

