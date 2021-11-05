from tests.mocks.command_run_mock import CommandRunMock

from src.command.apt import Apt


def test_interface_update(mocker):
    ''' Check argument construction for `apt update` '''
    with CommandRunMock(mocker, Apt(1).update) as call_args:
        assert call_args == ['apt', 'update']


def test_interface_download(mocker):
    ''' Check argument construction for `apt download package` '''
    with CommandRunMock(mocker, Apt(1).download, {'package': 'vim'}) as call_args:
        assert call_args == ['apt', 'download', 'vim']


def test_interface_install(mocker):
    ''' Check argument construction for `apt install -y package` '''
    with CommandRunMock(mocker, Apt(1).install, {'package': 'vim', 'assume_yes': True}) as call_args:
        assert call_args == ['apt', 'install', '-y', 'vim']
