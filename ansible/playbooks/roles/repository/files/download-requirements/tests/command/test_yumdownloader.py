from pathlib import Path

from tests.mocks.command_run_mock import CommandRunMock

from src.command.yumdownloader import Yumdownloader


def test_interface_download_packages(mocker):
    ''' Check argument construction for `yumdownloader` '''
    with CommandRunMock(mocker, Yumdownloader(1).download_packages, {'packages': [],
                                                                     'arch': 'some_arch',
                                                                     'destdir': Path('/some/path'),
                                                                     'exclude': '*'}) as call_args:
        assert call_args == ['yumdownloader', '-y', '--quiet', '--archlist=some_arch', '--exclude=*', '--destdir=/some/path']
