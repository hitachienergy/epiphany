import logging
import shutil
from pathlib import Path
from typing import List, Set

from src.command.command import Command
from src.config import Config
from src.error import PackageNotfound
from src.mode.base_mode import BaseMode


class RedHatFamilyMode(BaseMode):
    """
    Used by distros based of RedHat GNU/Linux
    """

    def __init__(self, config: Config):
        super().__init__(config)
        self.__base_packages: List[str] = ['yum-utils', 'wget', 'curl', 'tar']
        self.__installed_packages: List[str] = []

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
            if not Path('/etc/yum.repos.d/epel-testing.repo').exists() or not Path('/etc/yum.repos.d/epel.repo').exists():
                self._tools.yum.remove('epel-release')

        self._tools.yum.install('https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm')
        self.__installed_packages.append('epel-release')

        self.__remove_yum_cache_for_untracked_repos()
        self._tools.yum.makecache(True)

        for package in self.__base_packages:
            if not self._tools.rpm.is_package_installed(package):
                self._tools.yum.install(package)
                self.__installed_packages.append(package)

    def __enable_repos(self, repo_id_patterns: List[str]):
        for repo in self._tools.yum.find_rhel_repo_id(repo_id_patterns):
            if not self._tools.yum.is_repo_enabled(repo):
                self._tools.yum_config_manager.enable_repo(repo)

    def _add_third_party_repositories(self):
        # Fix for RHUI client certificate expiration [#2318]
        if self._tools.yum.is_repo_enabled('rhui-microsoft-azure-rhel'):
            self._tools.yum.update('rhui-microsoft-azure-rhel*')

        # -> rhel-7-server-extras-rpms # for container-selinux package, this repo has different id names on clouds
        # About rhel-7-server-extras-rpms: https://access.redhat.com/solutions/3418891
        repo_id_patterns = ['rhel-7-server-extras-rpms',
                            'rhui-rhel-7-server-rhui-extras-rpms',
                            'rhui-REGION-rhel-server-extras',
                            'rhel-7-server-rhui-extras-rpms']  # on-prem|Azure|AWS7.8|AWS7.9
        self.__enable_repos(repo_id_patterns)

        # -> rhel-server-rhscl-7-rpms # for Red Hat Software Collections (RHSCL), this repo has different id names on clouds
        # About rhel-server-rhscl-7-rpms: https://access.redhat.com/solutions/472793
        repo_id_patterns = ['rhel-server-rhscl-7-rpms',
                            'rhui-rhel-server-rhui-rhscl-7-rpms',
                            'rhui-REGION-rhel-server-rhscl',
                            'rhel-server-rhui-rhscl-7-rpms']  # on-prem|Azure|AWS7.8|AWS7.9
        self.__enable_repos(repo_id_patterns)

        for repo in self._repositories:
            repo_filepath = Path('/etc/yum.repos.d') / f'{repo}.repo'
            content = self._repositories[repo]['data']
            content = content + f'\ngpgkey={" ".join(self._repositories[repo]["gpg_keys"])}'

            if not self._tools.yum.is_repo_enabled(repo):
                with open(repo_filepath, mode='w') as repo_handler:
                    repo_handler.write(content)

                for key in self._repositories[repo]['gpg_keys']:
                    self._tools.rpm.import_key(key)

            self._tools.yum.accept_keys()

        # Official Docker CE repository, added with https://download.docker.com/linux/centos/docker-ce.repo,
        # has broken URL (https://download.docker.com/linux/centos/7Server/x86_64/stable) for longer time.
        # So direct (patched) link is used first if available.
        if self._tools.yum.is_repo_available('docker-ce-stable-patched'):
            self._tools.yum_config_manager.disable_repo('docker-ce-stable-patched')

            if not self._tools.yum.is_repo_enabled('docker-ce'):
                self._tools.yum_config_manager.add_repo('https://download.docker.com/linux/centos/docker-ce.repo')
                self._tools.yum.accept_keys()

        for repo in ['https://dl.2ndquadrant.com/default/release/get/10/rpm',  # for repmgr
                     'https://dl.2ndquadrant.com/default/release/get/13/rpm']:
            Command('curl', self._cfg.retries, [repo]) | Command('bash', self._cfg.retries)  # curl {repo} | bash

        # script adds 2 repositories, only 1 is required
        for repo in ['2ndquadrant-dl-default-release-pg10-debug',
                     '2ndquadrant-dl-default-release-pg13-debug']:
            self._tools.yum_config_manager.disable_repo(repo)

    def __remove_yum_cache_for_untracked_repos(self):
        # clean metadata for upgrades (when the same package can be downloaded from changed repo)

        whatprovides: List[str] = self._tools.rpm.which_packages_provides_file('system-release(releasever)')
        capabilities: List[str] = self._tools.rpm.get_package_capabilities(whatprovides[0])
        releasever: str = ''
        for cap in capabilities:
            if 'system-release(releasever)' in cap:
                releasever = cap.split('=')[-1].replace(' ', '')
                break

        cachedir: str = ''
        with open('/etc/yum.conf') as yum_conf:
            for line in yum_conf.readlines():
                if 'cachedir' in line:
                    cachedir = line.split('=')[-1].replace('\n', '')
                    break

        cachedir = cachedir.replace('$basearch', self._cfg.os_arch.value)
        cachedir = cachedir.replace('$releasever', releasever)

        cachedirs = [cdir for cdir in Path(cachedir).iterdir() if cdir.is_dir()]
        repoinfo: List[str] = self._tools.yum.list_all_repo_info()
        repoinfo = list(filter(lambda elem: 'Repo-id' in elem, repoinfo))
        repoinfo = [repo.split(':')[-1].replace(' ', '').split('/')[0] for repo in repoinfo]

        for cdir in cachedirs:
            if cdir.name in repoinfo:
                shutil.rmtree(str(cdir))

    def __download_prereq_packages(self) -> Set[str]:
        # download requirements (fixed versions)
        prereqs_dir = self._cfg.dest_packages / 'repo-prereqs'
        prereqs_dir.mkdir(exist_ok=True, parents=True)

        collected_prereqs: List[str] = []
        prereq_packages: List[str] = self._requirements['prereq-packages']
        for prereq_pkg in prereq_packages:
            collected_prereqs.extend(self._tools.repoquery.query(prereq_pkg,
                                                                 queryformat='%{ui_nevra}',
                                                                 arch=self._cfg.os_arch.value))

        unique_collected_prereqs: Set = set(collected_prereqs)
        for prereq in unique_collected_prereqs:
            self._tools.yumdownloader.download_packages([prereq],
                                                        arch=self._cfg.os_arch.value,
                                                        exclude='*i686',
                                                        destdir=prereqs_dir)
            logging.info(f'- {prereq}')

        return unique_collected_prereqs

    def _download_packages(self):
        downloaded_prereqs: Set = self.__download_prereq_packages()

        packages: List[str] = self._requirements['packages']
        packages_to_download: List[str] = []
        for package in packages:
            # package itself
            package_name = self._tools.repoquery.query(package,
                                                       queryformat='%{ui_nevra}',
                                                       arch=self._cfg.os_arch.value)[0]

            packages_to_download.append(package_name)

            # dependencies
            packages_to_download.extend(self._tools.repoquery.get_dependencies(package,
                                                                               queryformat='%{name}.%{arch}',
                                                                               arch=self._cfg.os_arch.value))

        for package in set(packages_to_download):
            if package not in downloaded_prereqs:
                logging.info(f'- {package}')
                self._tools.yumdownloader.download_packages([package],
                                                            arch=self._cfg.os_arch.value,
                                                            exclude='*i686',
                                                            destdir=self._cfg.dest_packages)

    def _download_file(self, file: str):
        output_path: Path = self._cfg.dest_packages if file.endswith('.rpm') else self._cfg.dest_files
        self._tools.wget.download(file, directory_prefix=output_path, additional_params=False)

    def _download_grafana_dashboard(self, dashboard: str, output_file: Path):
        self._tools.wget.download(dashboard, output_document=output_file, additional_params=False)

    def _download_crane_binary(self, url: str, dest: Path):
        self._tools.wget.download(url, dest, additional_params=False)

    def _cleanup(self):
        # remove repo files
        for repo_file in Path('/etc/yum.repos.d').iterdir():
            repo_file.unlink()

        # remove installed packages
        for package in self.__installed_packages:
            if self._tools.rpm.is_package_installed(package):
                self._tools.yum.remove(package)
