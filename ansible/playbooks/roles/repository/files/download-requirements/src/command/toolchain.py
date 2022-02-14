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
        self.__retries: int = retries

        self.crane = Crane(retries)
        self.tar = Tar()
        self.wget = Wget(retries)
        self.pip = Pip(retries)

    def _install_wget(self):
        """
        Used for offline mode to ensure that wget is installed on target OS.
        """
        raise NotImplementedError

    def ensure_pip(self):
        """
        Used for offline mode to ensure that pip is installed on target OS
        """

        try:  # check if pip is installed
            import pip
        except ModuleNotFoundError:  # pip missing
            self._install_wget()
            self.wget.download('https://bootstrap.pypa.io/get-pip.py', additional_params=False)
            Command('python3', self.__retries).run(['get-pip.py'])


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

    def _install_wget(self):
        self.yum.install('wget')


class DebianFamilyToolchain(Toolchain):
    """
    Specific tools used by Debian based distributions
    """

    def __init__(self, retries: int):
        super().__init__(retries)

        self.apt = Apt(retries)
        self.apt_cache = AptCache(retries)
        self.apt_key = AptKey(retries)

    def _install_wget(self):
        self.apt.install('wget')


TOOLCHAINS: Dict[OSType, Toolchain] = {
    OSType.RedHat: RedHatFamilyToolchain,
    OSType.Ubuntu: DebianFamilyToolchain
}
