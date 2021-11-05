import logging
from pathlib import Path
from typing import List

from src.command.command import Command
from src.command.toolchain import RedHatFamilyToolchain, Toolchain
from src.config import Config
from src.mode.base_mode import BaseMode


class RedHatFamilyMode(BaseMode):
    """
    Used by distros based of RedHat GNU/Linux
    """

    def __init__(self, config: Config):
        super().__init__(config)

    def _construct_toolchain(self) -> Toolchain:
        return RedHatFamilyToolchain(self._cfg.retries)

    def _use_backup_repositories(self):
        sources = Path('/etc/yum.repos.d/epirepo.repo')
        if not sources.exists() or not sources.stat().st_size:
            if self._cfg.repos_backup_file.exists() and self._cfg.enable_backup:
                logging.warn('OS repositories seems missing, restoring...')
                self._tools.tar.unpack(filename=self._cfg.repos_backup_file,
                                       target='.',
                                       directory=Path('/'),
                                       absolute_name=True,
                                       verbose=True)
            else:
                logging.warn(f'{str(sources)} seems to be missing, you either know what you are doing or '
                              'you need to fix your repositories')

    def __enable_repos(self, repo_id_patterns: List[str]):
        """
        :param repo_id_patterns:
        """
        for repo in self._tools.yum.find_rhel_repo_id(repo_id_patterns):
            if not self._tools.yum.is_repo_enabled(repo):
                self._tools.yum_config_manager.enable_repo(repo)

    def _add_third_party_repositories(self):
        # backup custom repositories to avoid possible conflicts
        for repo_file in Path('/etc/yum.repos.d/').iterdir():
            if repo_file.name.endswith('.repo'):
                repo_file.rename(f'{repo_file}.bak')

        # Fix for RHUI client certificate expiration [#2318]
        if self._tools.yum.is_repo_enabled('rhui-microsoft-azure-rhel'):
            self._tools.yum.update('rhui-microsoft-azure-rhel')

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
            content = content + f'\ngpgkey={" ".join(self._repositories[repo]["gpgkeys"])}'

            if not self._tools.yum.is_repo_enabled(repo):
                with open(repo_filepath, mode='w') as repo_handler:
                    repo_handler.write(content)

                for key in self._repositories[repo]['gpgkeys']:
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

        for repo in ['https://dl.2ndquadrant.com/default/release/get/10/rpm', # for repmgr
                     'https://dl.2ndquadrant.com/default/release/get/13/rpm']:
            Command('curl', self._cfg.retries, [repo]) | Command('bash', self._cfg.retries)  # curl {repo} | bash

        # script adds 2 repositories, only 1 is required
        for repo in ['2ndquadrant-dl-default-release-pg10-debug',
                     '2ndquadrant-dl-default-release-pg13-debug']:
            self._tools.yum_config_manager.disable_repo(repo)

    def _install_base_packages(self):
        # some packages are from EPEL repo
        if not self._tools.rpm.is_package_installed('epel-release'):
            self._tools.yum.install('https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm')

        # clean metadata for upgrades (when the same package can be downloaded from changed repo)
        # TODO remove_yum_cache_for_untracked_repos

        self._tools.yum.makecache(True)

        for package in ['yum-utils', 'wget', 'curl', 'tar']:
            if not self._tools.rpm.is_package_installed(package):
                self._tools.yum.install(package)

    def _download_packages(self):
        prereqs_dir = self._cfg.dest_packages / 'repo-prereqs'
        prereqs_dir.mkdir(exist_ok=True, parents=True)

        collected_prereqs: List[str] = []
        for prereq_pkg in self._requirements['prereq-packages']:
            collected_prereqs.append(self._tools.repoquery.query(prereq_pkg['name'],
                                                                 queryformat='%{ui_nevra}',
                                                                 arch=self._cfg.os_arch.value))

        # download requirements (fixed versions)
        if collected_prereqs:
            self._tools.yumdownloader.download_packages(collected_prereqs,
                                                        arch=self._cfg.os_arch.value,
                                                        exclude='*i686',
                                                        destdir=prereqs_dir)

    def _download_file(self, file: str):
        self._tools.wget.download(file, directory_prefix=self._cfg.dest_files, additional_params=False)

    def _download_dashboard(self, dashboard: str, output_file: Path):
        self._tools.wget.download(dashboard, output_document=output_file, additional_params=False)
