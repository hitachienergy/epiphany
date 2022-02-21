import logging
from collections import defaultdict
from os import chmod
from pathlib import Path
from typing import Any, Dict

from poyo import parse_string, PoyoException

from src.command.toolchain import Toolchain, TOOLCHAINS
from src.config import Config
from src.crypt import get_sha1, get_sha256
from src.error import CriticalError


def load_yaml_file(filename: Path) -> Any:
    try:
        with open(filename, encoding="utf-8") as req_handler:
            return parse_string(req_handler.read())
    except PoyoException as exc:
        logging.error(exc)
    except Exception:
        logging.error(f'Failed loading: {filename}')


class BaseMode:
    """
    An abstract class for running specific operations on target OS.
    Main running method is :func:`~base_mode.BaseMode.run`
    """

    def __init__(self, config: Config):
        self._cfg = config

        self._repositories: Dict[str, Dict] = self.__parse_repositories()
        self._requirements: Dict[str, Any] = self.__parse_requirements()
        self._tools: Toolchain = TOOLCHAINS[self._cfg.os_type](self._cfg.retries)

    def __parse_repositories(self) -> Dict[str, Dict]:
        """
        Load repositories for target architecture/distro from a yaml file.

        :returns: parsed repositories data
        """
        return load_yaml_file(self._cfg.repo_path / f'{self._cfg.distro_subdir}.yml')['repositories']

    def __parse_requirements(self) -> Dict[str, Any]:
        """
        Load requirements for target architecture/distro from a yaml file.

        :returns: parsed requirements data
        """
        reqs: Dict = defaultdict(dict)

        content = load_yaml_file(self._cfg.reqs_path / f'{self._cfg.distro_subdir}/packages.yml')
        reqs['packages'] = content['packages']

        try:
            reqs['prereq-packages'] = content['prereq-packages']
        except KeyError:
            pass  # prereq packages are only for some distros

        content = load_yaml_file(self._cfg.reqs_path / f'{self._cfg.distro_subdir}/files.yml')
        reqs['files'].update(content['files'])

        for common_reqs in ['cranes', 'files', 'images']:
            content = load_yaml_file(self._cfg.reqs_path / f'{self._cfg.os_arch.value}/{common_reqs}.yml')
            reqs[common_reqs].update(content[common_reqs])

        content = load_yaml_file(self._cfg.reqs_path / 'grafana-dashboards.yml')
        reqs['grafana-dashboards'].update(content['grafana-dashboards'])

        return reqs

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

    def __download_files(self):
        """
        Download files under `self._requirements['files']`
        """
        files: Dict[str, Dict] = self._requirements['files']
        for file in files:
            try:
                filepath = self._cfg.dest_files / file.split('/')[-1]
                if files[file]['sha256'] == get_sha256(filepath):
                    logging.debug(f'- {file} - checksum ok, skipped')
                    continue

                logging.info(f'- {file}')
                self._download_file(file)
            except CriticalError:
                logging.warn(f'Could not download file: {file}')

    def __download_grafana_dashboards(self):
        """
        Download grafana dashboards under `self._requirements['grafana-dashboards']`
        """
        dashboards: Dict[str, Dict] = self._requirements['grafana-dashboards']
        for dashboard in dashboards:
            try:
                output_file = self._cfg.dest_grafana_dashboards / f'{dashboard}.json'

                if dashboards[dashboard]['sha256'] == get_sha256(output_file):
                    logging.debug(f'- {dashboard} - checksum ok, skipped')
                    continue

                logging.info(f'- {dashboard}')
                self._download_grafana_dashboard(dashboards[dashboard]['url'], output_file)
            except CriticalError:
                logging.warn(f'Could not download grafana dashboard: {dashboard}')

    def __download_crane(self):
        """
        Download Crane package if needed and setup it's environment
        """
        crane_path = self._cfg.dest_dir / 'crane'
        crane_package_path = Path(f'{crane_path}.tar.gz')

        cranes = self._requirements['cranes']
        first_crane = next(iter(cranes))  # right now we use only single crane source
        if cranes[first_crane]['sha256'] == get_sha256(crane_package_path):
            logging.debug('crane - checksum ok, skipped')
        else:
            self._download_crane_binary(first_crane, crane_package_path)
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
        images = self._requirements['images']
        for image in images:
            try:
                url, version = image.split(':')
                filename = Path(f'{url.split("/")[-1]}-{version}.tar')  # format: image_version.tar

                if images[image]['sha1'] == get_sha1(self._cfg.dest_images / filename):
                    logging.debug(f'- {image} - checksum ok, skipped')
                    continue

                logging.info(f'- {image}')
                self._tools.crane.pull(image, self._cfg.dest_images / filename, platform)
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
            :class:`Exception`: on I/O OS failures
        """
        # add required directories
        self._cfg.dest_files.mkdir(exist_ok=True, parents=True)
        self._cfg.dest_grafana_dashboards.mkdir(exist_ok=True, parents=True)
        self._cfg.dest_images.mkdir(exist_ok=True, parents=True)
        self._cfg.dest_packages.mkdir(exist_ok=True, parents=True)

        logging.info('Checking backup repositories...')
        self._use_backup_repositories()
        logging.info('Done checking backup repositories.')

        logging.info('Installing base packages...')
        self._install_base_packages()
        logging.info('Done installing base packages.')

        logging.info('Adding third party repositories...')
        self._add_third_party_repositories()
        logging.info('Done adding third party repositories.')

        logging.info('Downloading packages...')
        self._download_packages()
        logging.info('Done downloading packages.')

        logging.info('Downloading files...')
        self.__download_files()
        logging.info('Done downloading files.')

        logging.info('Downloading grafana dashboards...')
        self.__download_grafana_dashboards()
        logging.info('Done downloading grafana dashboards.')

        logging.info('Downloading Crane...')
        self.__download_crane()
        logging.info('Done downloading Crane.')

        logging.info('Downloading images...')
        self._download_images()
        logging.info('Done downloading images.')

        logging.info('Running cleanup...')
        self._cleanup()
        logging.info('Done running cleanup.')
