from typing import Dict

from src.config.config import Config
from src.config.os_type import OSType
from src.mode.base_mode import BaseMode
from src.mode.debian_family_mode import DebianFamilyMode
from src.mode.red_hat_family_mode import RedHatFamilyMode


# Mapping for OSType -> Mode
MODES: Dict[OSType, BaseMode] = {
    OSType.Almalinux: RedHatFamilyMode,
    OSType.RHEL: RedHatFamilyMode,
    OSType.Ubuntu: DebianFamilyMode,
}


def run(config: Config):
    MODES[config.os_type](config).run()
