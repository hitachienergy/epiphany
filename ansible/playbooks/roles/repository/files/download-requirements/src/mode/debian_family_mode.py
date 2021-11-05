import logging
import os
from pathlib import Path
from shutil import move

from src.command.toolchain import DebianFamilyToolchain, Toolchain
from src.config import Config
from src.error import CriticalError
from src.mode.base_mode import BaseMode


class DebianFamilyMode(BaseMode):
    """
    Used by distros based of Debian GNU/Linux
    """

    def __init__(self, config: Config):
        super().__init__(config)

    def _construct_toolchain(self) -> Toolchain:
        return DebianFamilyToolchain(self._cfg.retries)

    def _add_third_party_repositories(self):
        # backup custom repositories to avoid possible conflicts
        for repo_file in Path('/etc/apt/sources.list.d').iterdir():
            if repo_file.name.endswith('.list'):
                repo_file.rename(f'{repo_file}.bak')

        # add third party keys
        for name, repo in self._repositories.items():
            key_file = Path(f'/tmp/{name}')
            self._tools.wget.download(repo.key, key_file)
            self._tools.apt_key.add(key_file)

        # create repo files
        for repo in self._repositories.values():
            with repo.path.open(mode='a') as repo_handler:
                repo_handler.write(repo.content)

        self._tools.apt.update()

    def _install_packages(self):
        # install prerequisites which might be missing
        installed_packages = self._tools.dpkg.list_installed_packages()

        logging.info('Installing base packages:')
        for package in ['wget', 'gpg', 'curl', 'tar']:
            if package not in installed_packages:
                self._tools.apt.install(package, assume_yes=True)
                logging.info(f'- {package}')

        logging.info('Done.')

        # path needs to be changed since `apt download` does not allow to set target dir
        os.chdir(self._cfg.dest_packages)

        logging.info('Downloading required packages:')
        for package in self._requirements['packages']:
            self._tools.apt.download(package)
            logging.info(f'- {package}')

        logging.info('Done.')

        os.chdir(self._cfg.script_path)

    def _download_files(self):
        for file in self._requirements['files']:
            try:
                self._tools.wget.download(file, directory_prefix=self._cfg.dest_files)
            except CriticalError:
                logging.warn(f'Could not download file: {file}')

    def _cleanup(self):
        # cleaning up 3rd party repositories
        for repo in self._repositories.values():
            if repo.path.exists():
                repo.path.unlink()

        # restore masked custom repositories to their original names
        for repo_file in Path('/etc/apt/sources.list.d').iterdir():
            if repo_file.name.endswith('.bak'):
                move(str(repo_file.absolute()), str(repo_file.with_suffix('').absolute()))
