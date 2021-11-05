import logging
from collections import defaultdict
from os import chmod
from pathlib import Path
from typing import Dict, List
from hashlib import sha256

import yaml

from src.command.toolchain import Toolchain
from src.config import Config
from src.error import CriticalError


def get_sha256(req_path: Path) -> str:
    """
    Calculate sha256 value for `req_path` file.

    :param req_path: of which file to calculate sha256
    :returns: calculated sha256 value, "-1" if file not found
    """
    try:
        with open(req_path, mode='rb') as req_file:
            shagen = sha256()
            shagen.update(req_file.read())
            return shagen.hexdigest()
    except FileNotFoundError:
        return "-1"


class BaseMode:
    """
    An abstract class for running specific operations on target OS.
    Main running method is :func:`~base_mode.BaseMode.run`
    """

    def __init__(self, config: Config):
        self._cfg = config

        self._repositories: Dict[str, Dict] = self.__parse_repositories()
        self._requirements: Dict[str, List[Dict]] = self.__parse_requirements()

        self._tools: Toolchain = self._construct_toolchain()

    def __parse_repositories(self) -> Dict[str, Dict]:
        """
        Load repositories for target architecture/distro from a yaml file.

        :returns: parsed repositories data
        """
        stream = open(self._cfg.repo_path / f'{self._cfg.distro_subdir}.yml')
        return yaml.safe_load(stream)['repositories']

    def __parse_requirements(self) -> Dict[str, List[Dict]]:
        """
        Load requirements for target architecture/distro from a yaml file.

        :returns: parsed requirements data
        """
        reqs = defaultdict(list)

        # target distro requirements
        stream = open(self._cfg.reqs_path / f'{self._cfg.distro_subdir}.yml')
        content = yaml.safe_load(stream)
        for key in content.keys():
            reqs[key].extend(content[key])

        for common_reqs in ['crane', 'files', 'images', 'dashboards']:
            stream = open(self._cfg.reqs_path / f'{common_reqs}.yml')
            content = yaml.safe_load(stream)
            reqs[common_reqs].extend(content[common_reqs])

        return reqs

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
        raise NotImplementedError

    def _add_third_party_repositories(self):
        """
        Add third party repositories for target OS's package manager
        """
        raise NotImplementedError

    def _install_base_packages(self):
        """
        Ensure that packages for file downloading are installed on the OS.
        """
        raise NotImplementedError

    def _download_packages(self):
        """
        Download packages under `self._requirements['packages']` using target OS's package manager
        """
        raise NotImplementedError

    def _download_file(self, file: str):
        """
        Run command for downloading `file` on target OS.

        :param file: to be downloaded
        """
        raise NotImplementedError

    def _download_dashboard(self, dashboard: str, output_file: Path):
        """
        Run command for downloading `dashboard` on target OS.

        :param dashboard: to be downloded
        :param output_file: under which filename dashboard will be saved
        """
        raise NotImplementedError

    def __download_files(self):
        """
        Download files under `self._requirements['files']`
        """
        for file in self._requirements['files']:
            try:
                filepath = self._cfg.dest_files / file['url'].split('/')[-1]
                if file['sha256'] == get_sha256(filepath):
                    logging.debug(f'- {file["url"]} - checksum ok, skipped')
                    continue

                logging.info(f'- {file["url"]}')
                self._download_file(file['url'])
            except CriticalError:
                logging.warn(f'Could not download file: {file["url"]}')

    def _download_dashboards(self):
        """
        Download dashboards under `self._requirements['dashboards']`
        """
        for dashboard in self._requirements['dashboards']:
            try:
                output_file = self._cfg.dest_dashboards / f'{dashboard["name"]}.json'

                if dashboard['sha256'] == get_sha256(output_file):
                    logging.debug(f'- {dashboard["name"]} - checksum ok, skipped')
                    continue

                logging.info(f'- {dashboard["name"]}')
                self._download_dashboard(dashboard['url'], output_file)
            except CriticalError:
                logging.warn(f'Could not download file: {dashboard["name"]}')

    def _download_crane(self):
        """
        Download Crane package if needed and setup it's environment
        """
        crane_path = self._cfg.dest_dir / 'crane'
        crane_package_path = Path(f'{crane_path}.tar.gz')

        if self._requirements['crane'][0]['sha256'] == get_sha256(crane_package_path):
            logging.debug(f'crane - checksum ok, skipped')
            return

        self._tools.wget.download(self._requirements['crane'][0]['url'], crane_package_path)
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
                url, version = image['name'].split(':')
                filename = Path(f'{url.split("/")[-1]}_{version}.tar')  # format: image_version.tar

                if image['sha256'] == get_sha256(self._cfg.dest_images / filename):
                    logging.debug(f'- {image["name"]} - checksum ok, skipped')
                    continue

                logging.info(f'- {image["name"]}')
                self._tools.crane.pull(image['name'], self._cfg.dest_images / filename, platform)
            except CriticalError:
                logging.warn(f'Could not download image: `{image["name"]}`')

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
            :class:`Exception`: on I/O OS failures
        """
        # add required directories
        self._cfg.dest_dashboards.mkdir(exist_ok=True, parents=True)
        self._cfg.dest_files.mkdir(exist_ok=True, parents=True)
        self._cfg.dest_images.mkdir(exist_ok=True, parents=True)
        self._cfg.dest_packages.mkdir(exist_ok=True, parents=True)

        logging.info('Checking backup repositories...')
        self._use_backup_repositories()
        logging.info('Done checking backup repositories.')

        logging.info('Adding third party repositories...')
        self._add_third_party_repositories()
        logging.info('Done adding third party repositories.')

        logging.info('Installing base packages...')
        self._install_base_packages()
        logging.info('Done installing base packages.')

        logging.info('Downloading packages...')
        self._download_packages()
        logging.info('Done downloading packages.')

        logging.info('Downloading files...')
        self.__download_files()
        logging.info('Done downloading files.')

        logging.info('Downloading dashboards...')
        self._download_dashboards()
        logging.info('Done downloading dashboards.')

        logging.info('Downloading Crane...')
        self._download_crane()
        logging.info('Done downloading Crane.')

        logging.info('Downloading images...')
        self._download_images()
        logging.info('Done downloading images.')

        logging.info('Running cleanup...')
        self._cleanup()
        logging.info('Done running cleanup.')
