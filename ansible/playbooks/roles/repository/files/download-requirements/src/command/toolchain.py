from src.command.apt import Apt
from src.command.apt_key import AptKey
from src.command.crane import Crane
from src.command.dpkg import Dpkg
from src.command.tar import Tar
from src.command.wget import Wget
from src.command.yum import Yum


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

        self.yum = Yum(retries)


class DebianFamilyToolchain(Toolchain):
    """
    Specific tools used by Debian based distributions
    """

    def __init__(self, retries: int):
        super().__init__(retries)

        self.apt = Apt(retries)
        self.apt_key = AptKey(retries)
        self.dpkg = Dpkg(retries)
