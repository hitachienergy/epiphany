import logging
from collections import defaultdict
from os import chmod
from pathlib import Path
from typing import Any, Dict

from src.command.toolchain import Toolchain, TOOLCHAINS
from src.config.config import Config, OSArch
from src.config.manifest_reader import load_yaml_file
from src.crypt import SHA_ALGORITHMS
from src.downloader.alt_addr_downloader import AltAddrDownloader
from src.downloader.downloader import Downloader
from src.error import CriticalError, ChecksumMismatch, RetriesExceeded


class BaseMode:
    """
    An abstract class for running specific operations on target OS.
    Main running method is :func:`~base_mode.BaseMode.run`
    """

    def __init__(self, config: Config):
        self._cfg = config

        self._repositories: Dict[str, Dict] = self.__parse_repositories()
        self._requirements: Dict[str, Any] = self.__parse_requirements()
        self._tools: Toolchain = TOOLCHAINS[self._cfg.os_type.os_family](self._cfg.retries)
        self._cfg.read_manifest(self._requirements)

    def __parse_repositories(self) -> Dict[str, Dict]:
        """
        Load repositories for target architecture/distro from a yaml file.

        :returns: parsed repositories data
        """
        common_repository_file = self._cfg.repo_path / f'{self._cfg.family_subdir}/{self._cfg.os_type.os_family.value}.yml'
        distro_repository_file = self._cfg.repo_path / f'{self._cfg.distro_subdir}/{self._cfg.os_type.os_name}.yml'

        repos: Dict[str, Dict] = {}
        if common_repository_file.exists():
            repos.update(load_yaml_file(common_repository_file)['repositories'])

        if distro_repository_file.exists():
            repos.update(load_yaml_file(distro_repository_file)['repositories'])

        if not repos:
            raise CriticalError('No repositories found')

        return repos

    def _parse_packages(self) -> Dict[str, Any]:
        """
        Load packages for target architecture/distro from yaml file(s).

        :returns: parsed packages data
        """
        raise NotImplementedError

    def __parse_requirements(self) -> Dict[str, Any]:
        """
        Load requirements for target architecture/distro from yaml files.

        :returns: parsed requirements data
        """
        reqs: Dict = defaultdict(dict)

        reqs.update(self._parse_packages())

        # parse distro files:
        distro_files: Path = self._cfg.reqs_path / f'{self._cfg.distro_subdir}/files.yml'
        if distro_files.exists():  # distro files are optional
            content = load_yaml_file(distro_files)
            reqs['files'].update(content['files'])

        # parse common arch files:
        for common_arch_reqs in ('cranes', 'files', 'images'):
            content = load_yaml_file(self._cfg.reqs_path / f'{self._cfg.os_arch.value}/{common_arch_reqs}.yml')
            reqs[common_arch_reqs].update(content[common_arch_reqs])

        content = load_yaml_file(self._cfg.reqs_path / 'grafana-dashboards.yml')
        reqs['grafana-dashboards'].update(content['grafana-dashboards'])

        return reqs

    def __check_connection(self, url: str) -> bool:
        try:
            if self._tools.wget.check_connection(url):
                return True
        except RetriesExceeded:
            logging.warning(f'Could not connect to: `{url}`')

        return False

    def _create_backup_repositories(self):
        """
        Create a backup of package repository files under the /etc directory.
        """
        raise NotImplementedError

    def _add_third_party_repositories(self):
        """
        Add third party repositories for target OS's package manager.
        """
        raise NotImplementedError

    def _install_base_packages(self):
        """
        Ensure that packages for file downloading are installed on the OS.
        """
        raise NotImplementedError

    def _download_packages(self):
        """
        Download packages `self._requirements['packages']['from_repo']` using target OS's package manager.
        """
        raise NotImplementedError

    def _download_file(self, url: str, dest: Path):
        """
        Run command for downloading `file` on target OS.

        :param url: to be downloaded
        :param path: where to save the file
        """
        raise NotImplementedError

    def _download_grafana_dashboard(self, dashboard: str, output_file: Path):
        """
        Run command for downloading `grafana dashboard` on target OS.

        :param dashboard: to be downloded
        :param output_file: under which filename dashboard will be saved
        """
        raise NotImplementedError

    def _download_crane_binary(self, url: str, dest: Path):
        """
        Run command for downloading `crane` on target OS.

        :param url: to be downloded
        :param dest: under which filename dashboard will be saved
        """
        raise NotImplementedError

    def __download_packages_from_urls(self, packages: Dict[str, Dict], dest: Path):
        """
        Download files under `self._requirements['packages']['from_url']`

        :param packages: to be downloaded
        :param dest: where to save the packages
        """
        downloader: Downloader = Downloader(packages, 'sha256', self._download_file)
        for package_file in packages:
            filepath = dest / package_file.split('/')[-1]
            downloader.download(package_file, filepath)

    def __download_file(self, files: Dict[str, Dict], req_file: str, downloader: AltAddrDownloader, dest: Path):
        """
        Download `req_file` using `downloader`.

        :param files: file entries from a requirements yaml
        :param req_file: entry from `files` to be downloaded
        :param downloader: wrapper to be used for downloading `req_file`
        :param dest: where to save the file
        """
        file_options = files[req_file]['options']
        for option_idx, option in enumerate(file_options):
            file_to_download = option['url']

            filepath = dest / file_to_download.split('/')[-1]
            if downloader.download(req_file, filepath, option_idx, 'url'):
                return

            if option_idx != len(file_options) - 1:
                logging.info('Trying different mirror...')

        raise CriticalError(f'No more addresses available for {req_file}')

    def __download_files(self, files: Dict[str, Dict], dest: Path):
        """
        Download files under `self._requirements['files']`

        :param files: to be downloaded
        :param dest: where to save the files
        """
        downloader: AltAddrDownloader = AltAddrDownloader(files, 'sha256', self._download_file,
                                                          check_connection=self.__check_connection)
        for req_file in files:
            self.__download_file(files, req_file, downloader, dest)

    def __download_grafana_dashboards(self):
        """
        Download grafana dashboards under `self._requirements['grafana-dashboards']`.
        """
        dashboards: Dict[str, Dict] = self._requirements['grafana-dashboards']
        downloader: Downloader = Downloader(dashboards, 'sha256', self._download_grafana_dashboard)
        for dashboard in dashboards:
            output_file = self._cfg.dest_grafana_dashboards / f'{dashboard}.json'
            downloader.download(dashboard, output_file, 'url')

    def __download_crane(self):
        """
        Download Crane package if needed and setup it's environment.
        """
        cranes = self._requirements['cranes']
        first_crane = next(iter(cranes))  # right now we use only single crane source

        crane_path = self._cfg.dest_dir / 'cranes'
        crane_bin_path = self._cfg.dest_dir / 'crane'
        crane_path.mkdir(exist_ok=True, parents=True)

        downloader: AltAddrDownloader = AltAddrDownloader(cranes, 'sha256', self._download_crane_binary,
                                                          check_connection=self.__check_connection)
        self.__download_file(cranes, first_crane, downloader, crane_path)

        if not (crane_path / 'crane').exists():
            # grab newest downloaded crane file:
            crane_file = sorted(list(crane_path.iterdir()), key=lambda crane: crane.stat().st_mtime)[0]

            self._tools.tar.unpack(crane_file, Path('crane'), directory=self._cfg.dest_dir)
            chmod(crane_bin_path, 0o0755)

        # create symlink to the crane file so that it'll be visible in shell
        crane_symlink = Path('/usr/bin/crane')
        if not crane_symlink.exists():
            crane_symlink.symlink_to(crane_bin_path)
            self._cfg.dest_crane_symlink = crane_symlink

    def _download_images(self):
        """
        Download images under `self._requirements['images']` using Crane.
        """
        platform: str = 'linux/amd64' if self._cfg.os_arch == OSArch.X86_64 else 'linux/arm64'
        images = self._requirements['images']

        images_to_download: Dict[str, Dict] = {}
        for image_group in images:  # kubernetes-master, rabbitmq, etc.
            for image, data in images[image_group].items():
                images_to_download[image] = data

        downloader: Downloader = Downloader(images_to_download,
                                            'sha1',
                                            self._tools.crane.pull,
                                            {'platform': platform})

        for image in images_to_download:
            url, version = image.split(':')
            filename = Path(f'{url.split("/")[-1]}-{version}.tar')  # format: image_version.tar

            image_file = self._cfg.dest_images / filename
            additional_args = {'use_legacy_format': False}

            if 'use_legacy_format' in images_to_download[image]:
                 additional_args['use_legacy_format'] = images_to_download[image]['use_legacy_format']

            downloader.download(image, image_file, additional_args=additional_args)

    def _cleanup(self):
        """
        Optional step for cleanup routines.
        """

    def _cleanup_packages(self):
        """
        Remove installed packages.
        """

    def _remove_repository_files(self):
        """
        Additional routines before unpacking backup to remove all repository files under the /etc directory.
        """

    def __restore_repositories(self):
        """
        Restore the state of repository files under the /etc dir.
        """
        if self._cfg.repos_backup_file.exists() and self._cfg.repos_backup_file.stat().st_size:
            logging.info('Restoring repository files...')
            self._remove_repository_files()
            self._tools.tar.unpack(filename=self._cfg.repos_backup_file,
                                   directory=Path('/'),
                                   absolute_names=True,
                                   uncompress=False,
                                   verbose=True)
            logging.info('Done restoring repository files.')

    def run(self):
        """
        Run target mode.

        :raises:
            :class:`CriticalError`: can be raised on exceeding retries
            :class:`Exception`: on I/O OS failures
        """
        # add required directories
        self._cfg.dest_files.mkdir(exist_ok=True, parents=True)
        self._cfg.dest_images.mkdir(exist_ok=True, parents=True)
        self._cfg.dest_packages.mkdir(exist_ok=True, parents=True)

        if self._requirements['grafana-dashboards']:
            self._cfg.dest_grafana_dashboards.mkdir(exist_ok=True, parents=True)

        # provides tar which is required for backup
        logging.info('Installing base packages...')
        self._install_base_packages()
        logging.info('Done installing base packages.')

        self._create_backup_repositories()

        if not self._cfg.was_backup_created:
            self.__restore_repositories()

        logging.info('Adding third party repositories...')
        self._add_third_party_repositories()
        logging.info('Done adding third party repositories.')

        logging.info('Downloading packages from repos...')
        self._download_packages()
        logging.info('Done downloading packages from repos.')

        logging.info('Downloading packages from urls...')
        self.__download_packages_from_urls(self._requirements['packages']['from_url'], self._cfg.dest_packages)
        logging.info('Done downloading packages from urls.')

        logging.info('Downloading files...')
        self.__download_files(self._requirements['files'], self._cfg.dest_files)
        logging.info('Done downloading files.')

        if self._requirements['grafana-dashboards']:
            logging.info('Downloading grafana dashboards...')
            self.__download_grafana_dashboards()
            logging.info('Done downloading grafana dashboards.')

        logging.info('Downloading Crane...')
        self.__download_crane()
        logging.info('Done downloading Crane.')

        logging.info('Downloading images...')
        self._download_images()
        logging.info('Done downloading images.')

        if self._cfg.dest_crane_symlink is not None:
            if self._cfg.dest_crane_symlink.exists():
                logging.debug(f'Removing `crane` symlink: {str(self._cfg.dest_crane_symlink)}...')
                self._cfg.dest_crane_symlink.unlink()
                logging.debug('Done.')

        logging.info('Running cleanup...')
        self._cleanup()
        logging.info('Done running cleanup.')

        # requires tar but has to be run after cleanup
        self.__restore_repositories()

        logging.info('Cleaning up installed packages...')
        self._cleanup_packages()
        logging.info('Done cleaning up installed packages.')
