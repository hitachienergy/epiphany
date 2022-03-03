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
             targets: List[Path],

             # short flags:
             compress: bool = False,
             verbose: bool = False,
             preserve: bool = False,

             # long flags:
             absolute_names: bool = False,
             directory: Path = None,
             verify: bool = False):
        """
        Create a tar archive.

        :param filename: name for the archive to be created
        :param targets: files to be archived

        :param compress: use zlib compression
        :param verbose: use verbose mode
        :param preserve: extract information about file permissions

        :param absolute_names: don't strip leading slashes from file names
        :param directory: change directory before doing any actions
        :param verify: check file integrity
        """
        short_flags: List[str] = ['-c']  # -czvf flags
        tar_params: List[str] = [str(filename)]  # all the other params

        # short flags:
        if compress:
            short_flags.append('z')

        if verbose:
            short_flags.append('v')

        if preserve:
            short_flags.append('p')

        short_flags.append('f')

        # long flags:
        if absolute_names:
            tar_params.append('--absolute-names')

        if directory is not None:
            tar_params.extend(['--directory', str(directory)])

        if verify:
            tar_params.append('--verify')

        for target in targets:
            tar_params.append(str(target))

        self.run([''.join(short_flags)] + tar_params)

    def unpack(self, filename: Path,
               target: Path = None,

               # short flags:
               uncompress: bool = True,
               verbose: bool = False,

               # long flags:
               absolute_names: bool = False,
               directory: Path = None,
               overwrite: bool = True,
               strip_components: int = 0):
        """
        Unpack a tar archive.

        :param filename: file to be extracted
        :param target: name for the output file

        :param uncompress: use zlib compression
        :param verbose: use verbose mode

        :param absolute_names: use abs path names
        :param directory: change directory before doing any actions
        :param overwrite: overwrite existing files when extracting
        :param strip_components: strip leading components from file names on extraction
        """
        short_flags: List[str] = ['-x']  # -xzvf flags
        tar_params: List[str] = [str(filename)]  # all the other params

        # short flags
        if uncompress:
            short_flags.append('z')

        if verbose:
            short_flags.append('v')

        short_flags.append('f')

        # long flags
        if absolute_names:
            tar_params.append('--absolute-names')

        if directory is not None:
            tar_params.extend(['--directory', str(directory)])

        if strip_components:
            tar_params.append(f'--strip-components={str(strip_components)}')

        if overwrite:
            tar_params.append('--overwrite')

        if target is not None:
            tar_params.append(str(target))

        self.run([''.join(short_flags)] + tar_params)
