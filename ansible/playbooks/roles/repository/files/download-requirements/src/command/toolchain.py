import logging
from typing import Dict

from src.command.crane import Crane
from src.command.debian.apt import Apt
from src.command.debian.apt_cache import AptCache
from src.command.debian.apt_key import AptKey
from src.command.redhat.dnf import Dnf
from src.command.redhat.dnf_config_manager import DnfConfigManager
from src.command.redhat.dnf_download import DnfDownload
from src.command.redhat.dnf_repoquery import DnfRepoquery
from src.command.redhat.rpm import Rpm
from src.command.tar import Tar
from src.command.wget import Wget
from src.config.os_type import OSFamily


class Toolchain:
    """
    Common tools used across all distributions
    """

    def __init__(self, retries: int):
        self.crane = Crane(retries)
        self.tar = Tar()
        self.wget = Wget(retries)

    @property
    def pyyaml_package(self) -> str:
        """
        Name of OS package that provides PyYAML
        """
        raise NotImplementedError

    def _install_pyyaml(self):
        """
        Used for offline mode, install PyYAML
        """
        raise NotImplementedError

    def uninstall_pyyaml(self):
        """
        Used for offline mode, uninstall PyYAML
        """
        raise NotImplementedError

    def ensure_pyyaml(self) -> bool:
        """
        Used for offline mode to ensure that PyYAML is available
        :returns: True - PyYAML had to be installed, False - PyYAML already present
        """
        try:  # check if PyYAML is available
            import yaml # pylint: disable=import-outside-toplevel,unused-import
            return False

        except ModuleNotFoundError:  # PyYAML missing
            logging.info(f'PyYAML not found, trying to install {self.pyyaml_package} package...')
            self._install_pyyaml()
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

    @property
    def pyyaml_package(self) -> str:
        return 'python3-pyyaml'

    def _install_pyyaml(self):
        self.dnf.install(self.pyyaml_package)

    def uninstall_pyyaml(self):
        self.dnf.remove(self.pyyaml_package)


class DebianFamilyToolchain(Toolchain):
    """
    Specific tools used by Debian based distributions
    """

    def __init__(self, retries: int):
        super().__init__(retries)

        self.apt = Apt(retries)
        self.apt_cache = AptCache(retries)
        self.apt_key = AptKey(retries)

    @property
    def pyyaml_package(self) -> str:
        return 'python3-yaml'

    def _install_pyyaml(self):
        self.apt.install(self.pyyaml_package)

    def uninstall_pyyaml(self):
        self.apt.remove(self.pyyaml_package)


TOOLCHAINS: Dict[OSFamily, Toolchain] = {
    OSFamily.Debian: DebianFamilyToolchain,
    OSFamily.RedHat: RedHatFamilyToolchain
}
