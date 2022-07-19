from pathlib import Path
from typing import Any, Dict, List
import logging
import os

from src.config.config import Config
from src.mode.base_mode import BaseMode, load_yaml_file, SHA_ALGORITHMS


class DebianFamilyMode(BaseMode):
    """
    Used by distros based of Debian GNU/Linux
    """

    def __init__(self, config: Config):
        super().__init__(config)
        self.__create_repo_paths()
        self.__installed_packages: List[str] = []

    def __create_repo_paths(self):
        for repo_id, repo_item in self._repositories.items():
            repo_item['path'] = Path('/etc/apt/sources.list.d') / f'{repo_id}.list'

    def _create_backup_repositories(self):
        if not self._cfg.repos_backup_file.exists():
            logging.debug('Creating backup for system repositories...')
            self._tools.tar.pack(self._cfg.repos_backup_file,
                                 targets=[Path('/etc/apt/sources.list'),
                                          Path('/etc/apt/sources.list.d')],
                                 verbose=True,
                                 preserve=True,
                                 absolute_names=True,
                                 verify=True)

            self._cfg.was_backup_created = True
            logging.debug('Done.')

    def _install_base_packages(self):
        # install prerequisites which might be missing
        installed_packages = self._tools.apt.list_installed_packages()

        # Ensure ca-certificates package is in the latest version
        self._tools.apt.install('ca-certificates')

        for package in ['wget', 'gpg', 'curl', 'tar']:
            if package not in installed_packages:
                self._tools.apt.install(package)
                self.__installed_packages.append(package)
                logging.info(f'- {package}')

    def _add_third_party_repositories(self):
        # add third party keys
        for repo, data in self._repositories.items():
            key_file = Path(f'/tmp/{repo}')
            self._tools.wget.download(data['key'], key_file)
            self._tools.apt_key.add(key_file)

        # create repo files
        for repo_file in self._repositories.values():
            with repo_file['path'].open(mode='a') as repo_handler:
                repo_handler.write(repo_file['content'])

        self._tools.apt.update()

    def _parse_packages(self) -> Dict[str, Any]:
        distro_level_file: Path = self._cfg.reqs_path / self._cfg.distro_subdir / 'packages.yml'
        distro_doc = load_yaml_file(distro_level_file)

        reqs: Dict = {
            'packages': distro_doc['packages']
        }

        return reqs

    def _download_packages(self):
        # path needs to be changed since `apt download` does not allow to set target dir
        os.chdir(self._cfg.dest_packages)

        packages: Dict[str, Dict] = self._requirements['packages']['from_repo']
        packages_to_download: List[str] = []
        for package in packages:
            version: str = ''
            try:
                package_base_name, version = package.split('=')  # some packages are in form of `package=version*`
            except ValueError:
                package_base_name = package

            package_info = self._tools.apt_cache.get_package_info(package_base_name, version)
            fetched_version = package_info['Version']

            # Files downloaded by `apt download` cannot have custom names
            # and they always starts with a package name + versioning and other info.
            # Find if there is a file corresponding with it's package name
            fetched_version_quoted = fetched_version.replace(':', '%3a')
            try:
                found_pkg: Path = [pkg_file for pkg_file in self._cfg.dest_packages.iterdir() if
                                   pkg_file.name.startswith(f'{package_info["Package"]}_') and
                                   fetched_version_quoted in pkg_file.name][0]

                if SHA_ALGORITHMS['sha256'](found_pkg) == package_info['SHA256']:
                    logging.debug(f'- {package} - checksum ok, skipped')
                    continue

            except IndexError:
                pass  # package not found

            # resolve dependencies for target package and if needed, download them first
            deps: List[str] = self._tools.apt_cache.get_package_dependencies(package_base_name, fetched_version)

            packages_to_download.extend(deps)
            packages_to_download.append(f'{package_base_name}={fetched_version}' if version else package_base_name)

        for package in sorted(set(packages_to_download)):
            logging.info(f'- {package}')
            self._tools.apt.download(package)

        os.chdir(self._cfg.script_path)

    def _download_file(self, url: str, dest: Path):
        self._tools.wget.download(url, output_document=dest)

    def _download_grafana_dashboard(self, dashboard: str, output_file: Path):
        self._tools.wget.download(dashboard, output_document=output_file)

    def _download_crane_binary(self, url: str, dest: Path):
        self._tools.wget.download(url, dest)

    def _remove_repository_files(self):
        logging.debug('Removing files from /etc/apt/sources.list.d...')
        for repo_file in Path('/etc/apt/sources.list.d').iterdir():
            logging.debug(f'- {repo_file.name}')
            repo_file.unlink()
        logging.debug('Done removing files.')

    def _cleanup(self):
        # cleaning up 3rd party repositories
        for data in self._repositories.values():
            if data['path'].exists():
                data['path'].unlink()

    def _cleanup_packages(self):
        for package in self.__installed_packages:
            self._tools.apt.remove(package)
