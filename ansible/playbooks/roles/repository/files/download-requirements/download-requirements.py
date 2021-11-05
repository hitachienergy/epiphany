#!/usr/bin/python3
import datetime
import logging
import sys
from os import getuid
from typing import Dict, List

from src.config import Config, OSType
from src.error import CriticalError
from src.mode.base_mode import BaseMode
from src.mode.debian_family_mode import DebianFamilyMode
from src.mode.red_hat_family_mode import RedHatFamilyMode


MODES: Dict[OSType, BaseMode] = {
    OSType.Ubuntu: DebianFamilyMode,
    OSType.RedHat: RedHatFamilyMode,
    OSType.CentOS: RedHatFamilyMode
}


def main(argv: List[str]) -> int:
    try:
        time_begin = datetime.datetime.now()
        if getuid() != 0:
            print('Error: Needs to be run as root!')
            return 1

        config = Config(argv)

        MODES[config.os_type](config).run()

        time_end = datetime.datetime.now() - time_begin
        logging.info(f'Total execution time: {str(time_end).split(".")[0]}')
    except CriticalError:
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
