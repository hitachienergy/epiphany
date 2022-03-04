import logging
from typing import Dict

from src.command.apt import Apt
from src.command.apt_cache import AptCache
from src.command.apt_key import AptKey
from src.command.command import Command
from src.command.crane import Crane
from src.command.pip import Pip
from src.command.dnf_repoquery import DnfRepoquery
from src.command.rpm import Rpm
from src.command.tar import Tar
from src.command.wget import Wget
from src.command.dnf import Dnf
from src.command.dnf_config_manager import DnfConfigManager
from src.command.dnf_download import DnfDownload
from src.config.os_type import OSFamily


class Toolchain:
    """
    Common tools used across all distributions
    """

    def __init__(self, retries: int):
        self.crane = Crane(retries)
        self.tar = Tar()
        self.wget = Wget(retries)
        self.pip = Pip(retries)

    def install_pip(self):
        """
        Used for offline mode, install pip package
        """
        raise NotImplementedError

    def uninstall_pip(self):
        """
        Used for offline mode, uninstall pip package
        """
        raise NotImplementedError

    def ensure_pip(self) -> bool:
        """
        Used for offline mode to ensure that pip is installed on target OS
        :returns: True - pip had to be installed, False - pip already installed
        """
        try:  # check if pip is installed
            import pip
            return False

        except ModuleNotFoundError:  # pip missing
            logging.info('pip3 not installed, try installing...')
            self.install_pip()
            logging.info('Done.')
            return True


class RedHatFamilyToolchain(Toolchain):
    """
    Specific tools used by RedHat based distributions
    """

    def __init__(self, retries: int):
        super().__init__(retries)

        self.repoquery = DnfRepoquery(retries)
        self.rpm = Rpm(retries)
        self.dnf = Dnf(retries)
        self.dnf_config_manager = DnfConfigManager(retries)
        self.dnf_download = DnfDownload(retries)

    def install_pip(self):
        self.dnf.install('python3-pip')

    def uninstall_pip(self):
        self.dnf.remove('python3-pip')


class DebianFamilyToolchain(Toolchain):
    """
    Specific tools used by Debian based distributions
    """

    def __init__(self, retries: int):
        super().__init__(retries)

        self.apt = Apt(retries)
        self.apt_cache = AptCache(retries)
        self.apt_key = AptKey(retries)

    def install_pip(self):
        self.apt.install('python3-pip')

    def uninstall_pip(self):
        self.apt.remove('python3-pip')


TOOLCHAINS: Dict[OSFamily, Toolchain] = {
    OSFamily.Debian: DebianFamilyToolchain,
    OSFamily.RedHat: RedHatFamilyToolchain
}
