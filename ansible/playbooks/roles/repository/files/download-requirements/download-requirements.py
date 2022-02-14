#!/usr/bin/python3
import datetime
import logging
from os import getuid
from typing import List

import sys

from src.command.toolchain import TOOLCHAINS
from src.config import Config, OSType
from src.error import CriticalError


def install_missing_modules(config: Config):
    """
    Install 3rd party missing modules.
    Used for offline mode.
    """
    tools = TOOLCHAINS[config.os_type](config.retries)
    tools.ensure_pip()
    tools.pip.install('poyo', '==0.5.0', user=True)


def main(argv: List[str]) -> int:
    try:
        time_begin = datetime.datetime.now()

        if getuid() != 0:
            print('Error: Needs to be run as root.')
            return 1

        config = Config(argv)

        try:  # make sure that 3rd party modules are installed
            from src.run import run
            run(config)

        except ModuleNotFoundError:
            install_missing_modules(config)

            from src.run import run
            run(config)  # try to rerun after installing missing modules

        time_end = datetime.datetime.now() - time_begin
        logging.info(f'Total execution time: {str(time_end).split(".")[0]}')
    except CriticalError:
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
