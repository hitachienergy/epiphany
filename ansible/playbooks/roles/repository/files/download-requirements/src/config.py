import logging
import os
import sys
from argparse import ArgumentParser, RawTextHelpFormatter
from enum import Enum
from pathlib import Path
from typing import List

from src.error import CriticalError


class OSType(Enum):
    """ Supported distribution types """
    Ubuntu='ubuntu'
    RedHat='redhat'
    CentOS='centos'


class OSArch(Enum):
    """ Supported architecture types """
    X86_64='x86_64'
    ARM64='arm64'


class Config:
    def __init__(self, argv: List[str]):
        self.dest_dashboards: Path
        self.dest_dir: Path
        self.dest_files: Path
        self.dest_images: Path
        self.dest_packages: Path
        self.distro_subdir: Path
        self.enable_backup: bool
        self.log_file: Path
        self.os_arch: OSArch
        self.os_type: OSType
        self.repo_path: Path
        self.repos_backup_file: Path
        self.reqs_path: Path
        self.retries: int
        self.script_path: Path

        self.__add_args(argv)
        self.__log_info_summary()

    def __log_info_summary(self):
        """
        Helper function for printing all parsed arguments
        """

        lines: List[str] = ['Info summary:']
        LINE_SIZE: int = 50
        lines.append('-' * LINE_SIZE)

        lines.append(f'OS Arch: {self.os_arch.value}')
        lines.append(f'OS Type: {self.os_type.value}')
        lines.append(f'Script location: {str(self.script_path.absolute())}')
        lines.append(f'Directories used:')
        lines.append(f'- dashboards: {str(self.dest_dashboards)}')
        lines.append(f'- files:      {str(self.dest_files)}')
        lines.append(f'- images:     {str(self.dest_images)}')
        lines.append(f'- packages:   {str(self.dest_packages)}')

        lines.append(f'Enable repos backup: {"Yes" if self.enable_backup else "No"}')
        if self.enable_backup:
            lines.append(f'Repos backup file: {str(self.repos_backup_file)}')

        lines.append(f'Log file location: {str(self.log_file.absolute())}')
        lines.append(f'Retries count: {self.retries}')

        lines.append('-' * LINE_SIZE)

        logging.info('\n'.join(lines))

    def __create_parser(self) -> ArgumentParser:
        parser = ArgumentParser(description='Download Requirements', formatter_class=RawTextHelpFormatter)

        # required arguments:
        parser.add_argument('destination_dir', metavar='DEST_DIR', type=Path, action='store', nargs='+',
                            help='requirements will be downloaded to this directory')
        parser.add_argument('os_type', metavar='OS_TYPE', type=str, action='store', nargs='+',
                            help='which of the supported OS will be used: (`centos`, `debian`, `redhat`, `detect`)\n'
                            'when using `detect`, script will try to find out which OS is being used')

        # optional arguments:
        parser.add_argument('--enable-repos-backup', '-b', action='store_true', dest='enable_backup', default=False,
                            help=('when used, backup archive for packages will be created and used')),
        parser.add_argument('--repos-backup-file', metavar='BACKUP_FILE', action='store',
                            dest='repos_backup_file', default='/var/tmp/enabled-system-repos.tar',
                            help='path to a backup file')
        parser.add_argument('--retries-count', '-r', metavar='COUNT', type=int, action='store', dest='retries',
                            default=3, help='how many retries before stopping operation')


        parser.add_argument('--log-file', '-l', metavar='LOG_FILE', type=Path, action='store', dest='log_file',
                            default=Path('./download-requirements.log'),
                            help='logs will be saved to this file')
        parser.add_argument('--log-level', metavar='LOG_LEVEL', type=str, action='store', dest='log_level',
                            default='info', help='set up log level, available levels: (`error`, `warn`, `info`, `debug`)')
        parser.add_argument('--no-logfile', action='store_true', dest='no_logfile',
                            help='no logfile will be created')

        return parser

    def __get_matching_os_type(self, os_type: str) -> OSType:
        """
        Check if the parsed OS type fits supported distributons.

        :param os_type: distro type to be checked
        :raise: on failure - CriticalError
        """

        for os in OSType:
            if os.value.upper() in os_type.upper():
                logging.info(f'Found Matching OS: `{os.value}`')
                return os

        raise CriticalError('Could not detect OS type')

    def __detect_os_type(self) -> OSType:
        """
        On most modern GNU/Linux OSs info about current distribution
        can be found at /etc/os-release.
        Check this file to find out on which distro this script is ran.
        """

        os_release = Path('/etc/os-relase')

        if os_release.exists():
            with open(os_release) as os_release_handler:
                for line in os_release_handler.readline():
                    if 'NAME' in line:
                        return self.__get_matching_os_type(line.split('=')[1])

        raise CriticalError('Could not detect OS type')

    def __setup_logger(self, log_level: str, log_file: Path, no_logfile: bool):
        # setup the logger:
        log_levels = {
            # map input log level to Python's logging library
            'error': logging.ERROR,
            'warn': logging.WARN,
            'info': logging.INFO,
            'debug': logging.DEBUG
        }

        log_format = '%(asctime)s [%(levelname)s]: %(message)s'

        # add stdout logger:
        logging.basicConfig(stream=sys.stdout, level=log_levels[log_level.lower()],
                            format=log_format)

        # add log file:
        if not no_logfile:
            root_logger = logging.getLogger()
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(log_levels[log_level.lower()])
            file_handler.setFormatter(logging.Formatter(fmt=log_format))
            root_logger.addHandler(file_handler)

    def __add_args(self, argv: List[str]):
        """
        Run the parser and add all of the arguments to the Config object.

        :param argv: input arguments to be parsed
        """

        self.script_path = Path(argv[0]).absolute().parents[0]
        self.repo_path = self.script_path / 'repositories'
        self.reqs_path = self.script_path / 'requirements'

        args = self.__create_parser().parse_args(argv[1:]).__dict__

        self.log_file = args['log_file']
        self.__setup_logger(args['log_level'], self.log_file, args['no_logfile'])

        # add required arguments:
        self.os_type = self.__detect_os_type() if args['os_type'][0] == 'detect' else self.__get_matching_os_type(args['os_type'][0])
        self.dest_dir = args['destination_dir'][0]
        self.dest_dashboards = self.dest_dir / 'dashboards'
        self.dest_files = self.dest_dir / 'files'
        self.dest_images = self.dest_dir / 'images'
        self.dest_packages = self.dest_dir / 'packages'

        # add optional arguments
        self.enable_backup = args['enable_backup']
        self.os_arch = OSArch(os.uname().machine)
        self.repos_backup_file = Path(args['repos_backup_file'])
        self.retries = args['retries']

        self.distro_subdir = Path(f'{self.os_arch.value}/{self.os_type.value}')
