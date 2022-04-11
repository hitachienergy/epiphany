from enum import Enum
from typing import Dict, List


class OSArch(Enum):
    """ Supported architecture types """
    X86_64 = 'x86_64'
    ARM64 = 'aarch64'


class OSFamily(Enum):
    """ Supported distro type families """
    Debian = 'debian'
    RedHat = 'redhat'


class OSConfig:
    """ Type used for describing OS configuration """
    def __init__(self, os_family: OSFamily, os_name: str, os_name_aliases: List[str] = None):
        self.family = os_family
        self.name = os_name
        self.aliases = os_name_aliases or []  # used when detecting os type with /etc/os-release


class OSType(Enum):
    """ Supported operating system types """
    Almalinux = OSConfig(OSFamily.RedHat, 'almalinux-8')
    RHEL = OSConfig(OSFamily.RedHat, 'rhel-8')
    Ubuntu = OSConfig(OSFamily.Debian, 'ubuntu-20.04')

    @property
    def os_family(self) -> OSFamily:
        return self.value.family

    @property
    def os_name(self) -> str:
        return self.value.name

    @property
    def os_aliases(self) -> List[str]:
        return self.value.aliases


# Supported operating systems:
SUPPORTED_OS_TYPES: Dict[OSArch, OSConfig] = {
    OSArch.X86_64: [
        OSType.Almalinux,
        OSType.RHEL,
        OSType.Ubuntu
    ],
    OSArch.ARM64: [
        OSType.Almalinux
    ]
}
