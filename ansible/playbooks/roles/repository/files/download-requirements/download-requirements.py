#!/usr/bin/python3
import datetime
import logging
from os import execv, getuid
from typing import List

import sys

from src.command.toolchain import TOOLCHAINS
from src.config.config import Config
from src.error import DownloadRequirementsError


def install_missing_modules(config: Config):
    """
    Install 3rd party missing modules.
    Used for offline mode.
    """
    tools = TOOLCHAINS[config.os_type](config.retries)
    config.pip_installed = tools.ensure_pip()
    config.poyo_installed = tools.pip.install('poyo', '==0.5.0', user=True)

    if config.poyo_installed:
        logging.debug('Installed `poyo==0.5.0` library')


def rerun_download_requirements(config: Config):
    """
    Rerun download-requirements after installing missing modules.
    This step is required because python interpreter needs to reload modules.
    Used for offline mode.
    """
    additional_args: List[str] = ['--rerun']

    # carry over info about installed 3rd party tools and modules:
    if config.pip_installed:
        additional_args.append('--pip-installed')

    if config.poyo_installed:
        additional_args.append('--poyo-installed')

    execv(__file__, sys.argv + additional_args)


def cleanup(config: Config):
    """
    Remove any 3rd party modules and tools.
    Used for offline mode.
    """
    tools = TOOLCHAINS[config.os_type.os_family](config.retries)

    if config.poyo_installed:
        logging.info('Uninstalling 3rd party python modules:')
        tools.pip.uninstall('poyo', '==0.5.0')
        logging.info('Done.')

    if config.pip_installed:
        logging.info('Uninstalling pip3...')
        tools.uninstall_pip()
        logging.info('Done.')


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
            rerun_download_requirements(config)

        cleanup(config)

        time_end = datetime.datetime.now() - time_begin
        logging.info(f'Total execution time: {str(time_end).split(".")[0]}')
    except DownloadRequirementsError:
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
