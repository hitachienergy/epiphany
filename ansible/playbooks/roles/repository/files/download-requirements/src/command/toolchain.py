import logging
from typing import Dict

from src.command.apt import Apt
from src.command.apt_cache import AptCache
from src.command.apt_key import AptKey
from src.command.command import Command
from src.command.crane import Crane
from src.command.pip import Pip
from src.command.repoquery import Repoquery
from src.command.rpm import Rpm
from src.command.tar import Tar
from src.command.wget import Wget
from src.command.yum import Yum
from src.command.yum_config_manager import YumConfigManager
from src.command.yumdownloader import Yumdownloader
from src.config import OSType


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
            self._install_pip()
            logging.info('Done.')
            return True


class RedHatFamilyToolchain(Toolchain):
    """
    Specific tools used by RedHat based distributions
    """

    def __init__(self, retries: int):
        super().__init__(retries)

        self.repoquery = Repoquery(retries)
        self.rpm = Rpm(retries)
        self.yum = Yum(retries)
        self.yum_config_manager = YumConfigManager(retries)
        self.yumdownloader = Yumdownloader(retries)

    def install_pip(self):
        self.yum.install('python3-pip')

    def uninstall_pip(self):
        self.yum.remove('python3-pip')


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


TOOLCHAINS: Dict[OSType, Toolchain] = {
    OSType.RedHat: RedHatFamilyToolchain,
    OSType.Ubuntu: DebianFamilyToolchain
}
