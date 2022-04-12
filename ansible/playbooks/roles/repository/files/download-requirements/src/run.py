from typing import Dict

from src.config import Config, OSType
from src.mode.base_mode import BaseMode
from src.mode.debian_family_mode import DebianFamilyMode
from src.mode.red_hat_family_mode import RedHatFamilyMode


MODES: Dict[OSType, BaseMode] = {
    OSType.Ubuntu: DebianFamilyMode,
    OSType.RedHat: RedHatFamilyMode,
}


def run(config: Config):
    MODES[config.os_type](config).run()
