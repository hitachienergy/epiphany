import logging
from os import chmod
from pathlib import Path
from typing import Any, Dict, List

from repositories.repositories import REPOSITORIES
from requirements.requirements import REQUIREMENTS
from src.command.toolchain import Toolchain
from src.config import Config
from src.error import CriticalError


class BaseMode:
    """
    An abstract class for running specific operations on target OS.
    Main running method is :func:`~base_mode.BaseMode.run`
    """

    def __init__(self, config: Config):
        self._cfg = config

        self._repositories: Dict[str, Any] = REPOSITORIES[self._cfg.os_arch][self._cfg.os_type]
        self._requirements: Dict[str, List] = REQUIREMENTS[self._cfg.os_arch][self._cfg.os_type]

        self._tools: Toolchain = self._construct_toolchain()

    def _construct_toolchain(self) -> Toolchain:
        """
        Setup suitable toolchain for target OS.

        :returns: newly constructed toolchain object
        """
        raise NotImplementedError

    def _use_backup_repositories(self):
        """
        Check if there were any critical issues and if so, try to restore the state using backup
        """
        if not Path('/etc/apt/sources.list').exists():
            if self._cfg.repos_backup_file.exists() and self._cfg.enable_backup:
                logging.warn('OS repositories seems missing, restoring...')
                self._tools.tar.unpack(filename=self._cfg.repos_backup_file,
                                       target='.',
                                       change_directory=Path('/'),
                                       absolute_name=True,
                                       verbose=True)
            else:
                logging.warn('/etc/apt/sources.list seems missing, you either know what you are doing or '
                             'you need to fix your repositories')

    def _add_third_party_repositories(self):
        """
        Add third party repositories for target OS's package manager
        """
        raise NotImplementedError

    def _install_packages(self):
        """
        Install packages under `self._requirements['packages']` using target OS's package manager
        """
        raise NotImplementedError

    def _download_files(self):
        """
        Download files under `self._requirements['files']`
        """
        raise NotImplementedError

    def _download_crane(self):
        """
        Download Crane package if needed and setup it's environment
        """
        crane_path = self._cfg.dest_dir / 'crane'
        crane_package_path = Path(f'{crane_path}.tar.gz')
        if not crane_path.exists():
            self._tools.wget.download(self._requirements['crane'][0], crane_package_path)
            self._tools.tar.unpack(crane_package_path, 'crane', directory=self._cfg.dest_dir)
            chmod(crane_path, 0o0755)

        # create symlink to the crane file so that it'll be visible in shell
        crane_symlink = Path('/usr/bin/crane')
        if not crane_symlink.exists():
            crane_symlink.symlink_to(crane_path)

    def _download_images(self):
        """
        Download images under `self._requirements['images']` using Crane
        """
        platform: str = 'linux/amd64' if self._cfg.os_arch.X86_64 else 'linux/arm64'
        for image in self._requirements['images']:
            try:
                self._tools.crane.pull(image, self._cfg.dest_files, platform)
            except CriticalError:
                logging.warn(f'Could not download image: `{image}`')

    def _cleanup(self):
        """
        Optional step for cleanup routines
        """
        pass

    def run(self):
        """
        Run target mode.

        :raises:
            :class:`CriticalError`: can be raised on exceeding retries
            Exception: on I/O OS failures
        """
        # add required directories
        self._cfg.dest_packages.mkdir(exist_ok=True, parents=True)
        self._cfg.dest_files.mkdir(exist_ok=True, parents=True)
        self._cfg.dest_images.mkdir(exist_ok=True, parents=True)

        logging.info('Checking backup repositories...')
        self._use_backup_repositories()
        logging.info('Done checking backup repositories.')

        logging.info('Adding third party repositories...')
        self._add_third_party_repositories()
        logging.info('Done adding third party repositories.')

        logging.info('Installing packages...')
        self._install_packages()
        logging.info('Done installing packages.')

        logging.info('Downloading files...')
        self._download_files()
        logging.info('Done downloading files.')

        logging.info('Downloading Crane...')
        self._download_crane()
        logging.info('Done downloading Crane.')

        logging.info('Downloading images...')
        self._download_images()
        logging.info('Done downloading images.')

        logging.info('Running cleanup...')
        self._cleanup()
        logging.info('Done running cleanup.')
