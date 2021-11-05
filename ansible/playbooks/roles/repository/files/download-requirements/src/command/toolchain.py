from src.command.apt import Apt
from src.command.apt_cache import AptCache
from src.command.apt_key import AptKey
from src.command.crane import Crane
from src.command.dpkg import Dpkg
from src.command.repoquery import Repoquery
from src.command.rpm import Rpm
from src.command.tar import Tar
from src.command.wget import Wget
from src.command.yum import Yum
from src.command.yum_config_manager import YumConfigManager
from src.command.yumdownloader import Yumdownloader


class Toolchain:
    """
    Common tools used across all distributions
    """

    def __init__(self, retries: int):
        self.crane = Crane(retries)
        self.tar = Tar()
        self.wget = Wget(retries)


class RedHatFamilyToolchain(Toolchain):
    """
    Specific tools used by RedHat based distributions
    """

    def __init__(self, retries: int):
        super().__init__(retries)

        self.repoquery = Repoquery(retries)
        self.rpm = Rpm(retries)
        self.yum = Yum(retries)
        self.yumdownloader = Yumdownloader(retries)
        self.yum_config_manager = YumConfigManager(retries)


class DebianFamilyToolchain(Toolchain):
    """
    Specific tools used by Debian based distributions
    """

    def __init__(self, retries: int):
        super().__init__(retries)

        self.apt = Apt(retries)
        self.apt_cache = AptCache(retries)
        self.apt_key = AptKey(retries)
        self.dpkg = Dpkg(retries)
