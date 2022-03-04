from pathlib import Path

from tests.mocks.command_run_mock import CommandRunMock

from src.command.dnf_download import DnfDownload


def test_interface_download_packages(mocker):
    ''' Check argument construction for `dnf download` '''
    with CommandRunMock(mocker, DnfDownload(1).download_packages, {'packages': [],
                                                                   'archlist': ['some_arch', 'noarch'],
                                                                   'destdir': Path('/some/path'),
                                                                   'exclude': '*'}) as call_args:
        assert call_args == ['dnf',
                             'download',
                             '--archlist=some_arch,noarch',
                             '--destdir=/some/path',
                             '--exclude=*',
                             '--quiet']
