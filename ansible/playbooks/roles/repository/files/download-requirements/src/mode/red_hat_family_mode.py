import configparser
import logging
import shutil
from pathlib import Path
from typing import Any, Dict, List

from src.command.command import Command
from src.config.config import Config
from src.mode.base_mode import BaseMode, load_yaml_file


class RedHatFamilyMode(BaseMode):
    """
    Used by distros based of RedHat GNU/Linux
    """

    def __init__(self, config: Config):
        super().__init__(config)
        self.__archs: List[str] = [config.os_arch.value, 'noarch']
        self.__base_packages: List[str] = ['curl', 'python3-dnf-plugins-core', 'wget']
        self.__installed_packages: List[str] = []
        self.__dnf_cache_path: Path = Path('/var/cache/dnf')

        try:
            dnf_config = configparser.ConfigParser()
            with Path('/etc/dnf/dnf.conf').open() as dnf_config_file:
                dnf_config.read(dnf_config_file)

            self.__dnf_cache_path = Path(dnf_config['main']['cachedir'])
        except FileNotFoundError:
            logging.debug('RedHatFamilyMode.__init__(): dnf config file not found')
        except configparser.Error as e:
            logging.debug(f'RedHatFamilyMode.__init__(): {e}')
        except KeyError:
            pass


    def _create_backup_repositories(self):
        if not self._cfg.repos_backup_file.exists() or not self._cfg.repos_backup_file.stat().st_size:
            logging.debug('Creating backup for system repositories...')
            self._tools.tar.pack(self._cfg.repos_backup_file,
                                 [Path('/etc/yum.repos.d/')],
                                 verbose=True,
                                 directory=Path('/'),
                                 verify=True)

            self._cfg.was_backup_created = True
            logging.debug('Done.')

    def _install_base_packages(self):
        # some packages are from EPEL repo
        # make sure that we reinstall it before proceeding
        if self._tools.rpm.is_package_installed('epel-release'):
            if not self._tools.dnf.is_repo_enabled('epel') or not self._tools.dnf.is_repo_enabled('epel-modular'):
                self._tools.dnf.remove('epel-release')

        self._tools.dnf.install('https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm')
        self.__installed_packages.append('epel-release')

        self.__remove_dnf_cache_for_custom_repos()
        self._tools.dnf.makecache(True)

        # tar does not come by default from image. We install it, but don't want to remove it
        if not self._tools.rpm.is_package_installed('tar'):
            self._tools.dnf.install('tar')

        for package in self.__base_packages:
            if not self._tools.rpm.is_package_installed(package):
                self._tools.dnf.install(package)
                self.__installed_packages.append(package)

    def _add_third_party_repositories(self):
        # Fix for RHUI client certificate expiration [#2318]
        if self._tools.dnf.is_repo_enabled('rhui-microsoft-azure-rhel'):
            self._tools.dnf.update(enablerepo='rhui-microsoft-azure-rhel*')

        for repo in self._repositories:
            repo_filepath = Path('/etc/yum.repos.d') / f'{repo}.repo'
            content = [f'[{self._repositories[repo]["id"]}]',
                       self._repositories[repo]['data'],
                       f'gpgkey={" ".join(self._repositories[repo]["gpg_keys"])}']

            if not self._tools.dnf.is_repo_enabled(repo):
                with open(repo_filepath, mode='w') as repo_handler:
                    repo_handler.write('\n'.join(content))

                for key in self._repositories[repo]['gpg_keys']:
                    self._tools.rpm.import_key(key)

            self._tools.dnf.accept_keys()

        if not self._tools.dnf.is_repo_enabled('docker-ce'):
            self._tools.dnf_config_manager.add_repo('https://download.docker.com/linux/centos/docker-ce.repo')
            self._tools.dnf.accept_keys()

        for repo in ['https://dl.2ndquadrant.com/default/release/get/10/rpm',  # for repmgr
                     'https://dl.2ndquadrant.com/default/release/get/13/rpm']:
            Command('curl', self._cfg.retries, [repo]) | Command('bash', self._cfg.retries)  # curl {repo} | bash

        # script adds 2 repositories, only 1 is required
        for repo in ['2ndquadrant-dl-default-release-pg10-debug',
                     '2ndquadrant-dl-default-release-pg13-debug']:
            self._tools.dnf_config_manager.disable_repo(repo)

    def __remove_dnf_cache_for_custom_repos(self):
        # clean metadata for upgrades (when the same package can be downloaded from changed repo)
        repocaches: List[str] = list(self.__dnf_cache_path.iterdir())

        id_names = [
            '2ndquadrant',
            'docker-ce',
            'epel',
        ] + [self._repositories[key]['id'] for key in self._repositories.keys()]

        for repocache in repocaches:
            matched_ids = [repocache.name.startswith(repo_name) for repo_name in id_names]
            if any(matched_ids):
                try:
                    if repocache.is_dir():
                        shutil.rmtree(str(repocache))
                    else:
                        repocache.unlink()
                except FileNotFoundError:
                    logging.debug('__remove_dnf_cache_for_custom_repos: cache directory already removed')

    def _parse_packages(self) -> Dict[str, Any]:
        distro_level_file: Path = self._cfg.reqs_path / self._cfg.distro_subdir / 'packages.yml'
        family_level_file: Path = self._cfg.reqs_path / self._cfg.family_subdir / 'packages.yml'

        distro_doc = load_yaml_file(distro_level_file)
        family_doc = load_yaml_file(family_level_file)

        reqs: Dict = {
            'packages': distro_doc['packages'],
            'prereq-packages': distro_doc['prereq-packages'] + family_doc['prereq-packages']
        }

        reqs['packages']['from_repo'] += family_doc['packages']['from_repo']

        # distro level has precedence
        reqs['packages']['from_url'] = {**family_doc['packages']['from_url'], **distro_doc['packages']['from_url']}

        return reqs

    def __download_prereq_packages(self) -> List[str]:
        # download requirements (fixed versions)
        prereqs_dir = self._cfg.dest_packages / 'repo-prereqs'
        prereqs_dir.mkdir(exist_ok=True, parents=True)

        prereq_packages: List[str] = sorted(set(self._requirements['prereq-packages']))

        collected_prereqs: List[str] = self._tools.repoquery.query(prereq_packages,
                                                                   queryformat='%{name}-%{version}-%{release}.%{arch}',
                                                                   archlist=self.__archs)

        logging.info('- prereq-packages to download: %s', collected_prereqs)

        self._tools.dnf_download.download_packages(collected_prereqs,
                                                   archlist=self.__archs,
                                                   exclude='*i686',
                                                   destdir=prereqs_dir)
        return collected_prereqs

    def _download_packages(self):
        downloaded_prereq_packages: List[str] = self.__download_prereq_packages()

        packages: List[str] = sorted(set(self._requirements['packages']['from_repo']))

        # packages
        queried_packages: List[str] = self._tools.repoquery.query(packages,
                                                                  queryformat='%{name}-%{version}-%{release}.%{arch}',
                                                                  archlist=self.__archs)

        packages_to_download: List[str] = sorted(set(queried_packages) - set(downloaded_prereq_packages))

        logging.info('- packages to download: %s', packages_to_download)

        # dependencies
        dependencies: List[str] = self._tools.repoquery.get_dependencies(packages_to_download,
                                                                         queryformat='%{name}.%{arch}',
                                                                         archlist=self.__archs)

        logging.info('- dependencies to download: %s', dependencies)

        packages_to_download = sorted(packages_to_download + dependencies)

        self._tools.dnf_download.download_packages(packages_to_download,
                                                   archlist=self.__archs,
                                                   exclude='*i686',
                                                   destdir=self._cfg.dest_packages)

    def _download_file(self, url: str, dest: Path):
        self._tools.wget.download(url, output_document=dest, additional_params=False)

    def _download_grafana_dashboard(self, dashboard: str, output_file: Path):
        self._tools.wget.download(dashboard, output_document=output_file, additional_params=False)

    def _download_crane_binary(self, url: str, dest: Path):
        self._tools.wget.download(url, dest, additional_params=False)

    def _clean_up_repository_files(self):
        for repofile in Path('/etc/yum.repos.d').iterdir():
            repofile.unlink()

    def _cleanup(self):
        # remove installed packages
        for package in self.__installed_packages:
            if self._tools.rpm.is_package_installed(package):
                self._tools.dnf.remove(package)

        self.__remove_dnf_cache_for_custom_repos()
