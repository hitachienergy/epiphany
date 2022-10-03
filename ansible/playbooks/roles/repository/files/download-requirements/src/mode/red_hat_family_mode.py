import configparser
import logging
import shutil
from pathlib import Path
from typing import Any, Dict, List, Set

from src.command.command import Command
from src.config.config import Config
from src.config.os_type import OSArch
from src.mode.base_mode import BaseMode, load_yaml_file


class RedHatFamilyMode(BaseMode):
    """
    Used by distros based of RedHat GNU/Linux
    """

    def __init__(self, config: Config):
        super().__init__(config)
        self.__all_queried_packages: Set[str] = set()
        self.__archs: List[str] = [config.os_arch.value, 'noarch']
        self.__base_packages: List[str] = ['curl', 'python3-dnf-plugins-core', 'wget', 'tar']
        self.__dnf_cache_dir: Path = Path('/var/cache/dnf')
        self.__installed_packages: List[str] = []

        try:
            dnf_config = configparser.ConfigParser()
            with Path('/etc/dnf/dnf.conf').open(encoding='utf-8') as dnf_config_file:
                dnf_config.read(dnf_config_file)

            self.__dnf_cache_dir = Path(dnf_config['main']['cachedir'])
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
        # Ensure `dnf config-manager` command
        if not self._tools.rpm.is_package_installed('dnf-plugins-core'):
            self._tools.dnf.install('dnf-plugins-core')
            self.__installed_packages.append('dnf-plugins-core')

        # Bug in RHEL 8.4 https://bugzilla.redhat.com/show_bug.cgi?id=2004853
        releasever = '8' if self._tools.dnf_config_manager.get_variable('releasever') == '8.4' else None
        self._tools.dnf.update(package='libmodulemd', releasever=releasever)

        # epel-release package is re-installed when repo it provides is not enabled
        epel_package_initially_present: bool = self._tools.rpm.is_package_installed('epel-release')

        if epel_package_initially_present and not self._tools.dnf.are_repos_enabled(['epel', 'epel-modular']):
            self._tools.dnf.remove('epel-release')

        # some packages are from EPEL repo, ensure the latest version
        if not self._tools.rpm.is_package_installed('epel-release'):
            self._tools.dnf.install('https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm')

            if not epel_package_initially_present:
                self.__installed_packages.append('epel-release')
        else:
            self._tools.dnf.update('https://dl.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm',
                                   ignore_already_installed_error=True)

        self.__remove_dnf_cache_for_custom_repos()
        self._tools.dnf.makecache(timer=True)

        # Ensure ca-certificates package is in the latest version
        self._tools.dnf.install('ca-certificates', ignore_already_installed_error=True)

        for package in self.__base_packages:
            if not self._tools.rpm.is_package_installed(package):
                self._tools.dnf.install(package)
                self.__installed_packages.append(package)

    def _add_third_party_repositories(self):
        # Fix for RHUI client certificate expiration [#2318]
        if self._tools.dnf.is_repo_enabled('rhui-microsoft-azure-rhel'):
            self._tools.dnf.update(disablerepo='*', enablerepo='rhui-microsoft-azure-rhel*')

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

        # repmgr is supported only with x86_64 architecture
        if self._cfg.os_arch == OSArch.X86_64:
            for repo in ('https://dl.2ndquadrant.com/default/release/get/10/rpm',  # for repmgr
                         'https://dl.2ndquadrant.com/default/release/get/13/rpm'):
                Command('curl', self._cfg.retries, [repo]) | Command('bash', self._cfg.retries)  # curl {repo} | bash

            # script adds 2 repositories, only 1 is required
            for repo in ('2ndquadrant-dl-default-release-pg10-debug',
                         '2ndquadrant-dl-default-release-pg13-debug'):
                self._tools.dnf_config_manager.disable_repo(repo)

        self._tools.dnf.makecache(False, True)

    def __remove_dnf_cache_for_custom_repos(self):
        # clean metadata for upgrades (when the same package can be downloaded from changed repo)
        cache_paths: List[Path] = list(self.__dnf_cache_dir.iterdir())

        def get_matched_paths(repo_id: str, paths: List[Path]) -> List[Path]:
            return [path for path in paths if path.name.startswith(repo_id)]

        repo_ids = [
            '2ndquadrant',
            'docker-ce',
            'epel',
        ] + [repo['id'] for repo in self._repositories.values()]

        matched_cache_paths: List[Path] = []

        for repo_id in repo_ids:
            matched_cache_paths.extend(get_matched_paths(repo_id, cache_paths))

        if matched_cache_paths:
            matched_cache_paths.sort()
            logging.debug(f'Removing DNF cache files from {self.__dnf_cache_dir}...')

        for path in matched_cache_paths:
                logging.debug(f'- {path.name}')
                try:
                    if path.is_dir():
                        shutil.rmtree(str(path))
                    else:
                        path.unlink()
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
        reqs['packages']['multiple_versioned'] += family_doc['packages']['multiple_versioned']

        # distro level has precedence
        reqs['packages']['from_url'] = {**family_doc['packages']['from_url'], **distro_doc['packages']['from_url']}

        return reqs

    def __download_prereq_packages(self):
        # download requirements (fixed versions)
        prereqs_dir = self._cfg.dest_packages / 'repo-prereqs'
        prereqs_dir.mkdir(exist_ok=True, parents=True)

        prereq_packages: List[str] = sorted(set(self._requirements['prereq-packages']))

        collected_prereqs: List[str] = self._tools.repoquery.query(prereq_packages,
                                                                   queryformat='%{name}-%{version}-%{release}.%{arch}',
                                                                   archlist=self.__archs)

        logging.info(f'- prereq-packages to download: {collected_prereqs}')

        self._tools.dnf_download.download_packages(collected_prereqs,
                                                   archlist=self.__archs,
                                                   exclude='*i686',
                                                   destdir=prereqs_dir)

        self.__all_queried_packages.update(collected_prereqs)

    def __download_redhat_packages(self, packages: List[str], only_newest: bool = True):
        # packages
        queried_packages: List[str] = self._tools.repoquery.query(packages,
                                                                  queryformat='%{name}-%{version}-%{release}.%{arch}',
                                                                  archlist=self.__archs,
                                                                  only_newest=only_newest)

        packages_to_download: List[str] = sorted(set(queried_packages) - self.__all_queried_packages)

        logging.info(f'- packages to download: {packages_to_download}')

        # dependencies
        dependencies: List[str] = self._tools.repoquery.get_dependencies(packages_to_download,
                                                                         queryformat='%{name}.%{arch}',
                                                                         archlist=self.__archs,
                                                                         only_newest=only_newest)

        logging.info(f'- dependencies to download: {dependencies}')

        packages_to_download = sorted(packages_to_download + dependencies)
        self.__all_queried_packages.update(packages_to_download)

        self._tools.dnf_download.download_packages(packages_to_download,
                                                   archlist=self.__archs,
                                                   exclude='*i686',
                                                   destdir=self._cfg.dest_packages)

    def _download_packages(self):
        self.__download_prereq_packages()
        self.__download_redhat_packages(sorted(set(self._requirements['packages']['from_repo'])))
        self.__download_redhat_packages(sorted(set(self._requirements['packages']['multiple_versioned'])),
                                        False)

    def _download_file(self, url: str, dest: Path):
        self._tools.wget.download(url, output_document=dest, additional_params=False)

    def _download_grafana_dashboard(self, dashboard: str, output_file: Path):
        self._tools.wget.download(dashboard, output_document=output_file, additional_params=False)

    def _download_crane_binary(self, url: str, dest: Path):
        self._tools.wget.download(url, dest, additional_params=False)

    def _remove_repository_files(self):
        logging.debug('Removing files from /etc/yum.repos.d...')
        for repo_file in Path('/etc/yum.repos.d').iterdir():
            logging.debug(f'- {repo_file.name}')
            repo_file.unlink()
        logging.debug('Done removing files.')

    def _cleanup(self):
        self.__remove_dnf_cache_for_custom_repos()

    def _cleanup_packages(self):
        for package in self.__installed_packages:
            if self._tools.rpm.is_package_installed(package):
                self._tools.dnf.remove(package)
