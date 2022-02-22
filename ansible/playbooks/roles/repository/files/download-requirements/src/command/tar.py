from pathlib import Path
from typing import List

from src.command.command import Command


class Tar(Command):
    """
    Interface for `tar`
    """

    def __init__(self):
        super().__init__('tar', 1)

    def pack(self, filename: Path,
             target: str,
             directory: Path = None,
             verbose: bool = False,
             compress: bool = False,
             verify: bool = False):
        """
        Create a tar archive

        :param filename: name for the archive to be created
        :param target: files to be archived
        :param directory: change directory before doing any actions
        :param verbose: use verbose mode
        :param uncompress: use zlib compression
        :param verify: check file integrity
        """
        short_flags: List[str] = ['-c']  # -czvf flags
        tar_params: List[str] = [str(filename)]  # all the other params

        if compress:
            short_flags.append('z')

        if verbose:
            short_flags.append('v')

        short_flags.append('f')

        if verify:
            tar_params.append('--verify')

        if directory is not None:
            tar_params.extend(['--directory', str(directory)])

        if target:
            tar_params.append(target)

        self.run([''.join(short_flags)] + tar_params)

    def unpack(self, filename: Path,
               target: str = '',
               absolute_names: bool = False,
               directory: Path = None,
               overwrite: bool = True,
               strip_components: int = 0,
               uncompress: bool = True,
               verbose: bool = False):
        """
        Unpack a tar archive

        :param filename: file to be extracted
        :param target: name for the output file
        :param absolute_names: use abs path names
        :param directory: change directory before doing any actions
        :param overwrite: overwrite existing files when extracting
        :param strip_components: strip leading components from file names on extraction
        :param uncompress: use zlib compression
        :param verbose: use verbose mode
        """
        short_flags: List[str] = ['-x']  # -xzvf flags
        tar_params: List[str] = [str(filename)]  # all the other params

        if uncompress:
            short_flags.append('z')

        if verbose:
            short_flags.append('v')

        short_flags.append('f')

        if absolute_names:
            tar_params.append('--absolute-names')

        if directory is not None:
            tar_params.extend(['--directory', str(directory)])

        if strip_components:
            tar_params.append(f'--strip-components={str(strip_components)}')

        if target:
            tar_params.append(target)

        if overwrite:
            tar_params.append('--overwrite')

        self.run([''.join(short_flags)] + tar_params)
